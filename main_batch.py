import datetime
import sys 
import math
import os
import pathlib
from functools import partial
import warnings
import pdb 
import pandas as pd

from datasets.dataset import MyDataset
import torch.multiprocessing as mp
from joblib import Memory
from num2words import num2words
import numpy as np
from omegaconf import OmegaConf
from rich.console import Console
from torch.utils.data import DataLoader
from tqdm import tqdm
from typing import List
from configs import config
from utils import seed_everything
import datasets
import json 
from vision_models import CodexModel
from vision_processes import finish_all_consumers
# See https://github.com/pytorch/pytorch/issues/11201, https://github.com/pytorch/pytorch/issues/973
# Not for dataloader, but for multiprocessing batches
# mp.set_sharing_strategy('file_system')
queue_results = None
from image_patch import ImagePatch
cache = Memory('cache/' if config.use_cache else None, verbose=0)
runs_dict = {}
seed_everything()
console = Console(highlight=False)


def my_collate(batch):
    # Avoid stacking images (different size). Return everything as a list
    to_return = {k: [d[k] for d in batch] for k in batch[0].keys()}
    return to_return


def run_program(parameters, queues_in_, input_type_, retrying=False):
    from image_patch import ImagePatch, llm_query, best_image_match, distance, bool_to_yesno
    from video_segment import VideoSegment

    global queue_results

    

    c,image_path,image_id,query = parameters

    code_header = f"console.print(list(globals().keys()))\nfrom image_patch import ImagePatch\nfrom PIL import Image\nconsole.print('I made it')\nimage = Image.open('{image_path}').convert('RGB')\n"
    code_end = f"answer = execute_command(image)"
    all_code = code_header+c+'\n'+code_end
    console.print(all_code)
    return_dict = {}
    exec(all_code,globals(),return_dict)
    # code_header = f'def execute_command_{index}(' \
    #               f'{input_type_}, possible_answers, query, ' \
    #               f'ImagePatch, VideoSegment, ' \
    #               'llm_query, bool_to_yesno, distance, best_image_match):\n' \
    #               f'    # Answer is:'
    # code = code_header + code
    # y =  exec(compile(code, 'Codex', 'exec'), globals())
    # console.print(y,'output')
    # try:
    #     console.print('am trying to execute')
    #     exec(compile(code, 'Codex', 'exec'), globals())
        
    # except Exception as e:
    #     print(f'Sample {index} failed at compilation time with error: {e}')
    #     try:
    #         with open(config.fixed_code_file, 'r') as f:
    #             fixed_code = f.read()
    #         code = code_header + fixed_code 
    #         exec(compile(code, 'Codex', 'exec'), globals())
    #     except Exception as e2:
    #         print(f'Not even the fixed code worked. Sample {index} failed at compilation time with error: {e2}')
    #         return None, code

    # queues = [queues_in_, queue_results]

    # image_patch_partial = partial(ImagePatch, queues=queues)
    # video_segment_partial = partial(VideoSegment, queues=queues)
    # llm_query_partial = partial(llm_query, queues=queues)

    # try:
    #     result = globals()[f'execute_command_{index}'](
    #         # Inputs to the function
    #         image, 'yes', query,
    #         # Classes to be used
    #         image_patch_partial, video_segment_partial,
    #         # Functions to be used
    #         llm_query_partial, bool_to_yesno, distance, best_image_match)
    # except Exception as e:
    #     if retrying:
    #         return None, code
    #     print(f'Sample {index} failed with error: {e}. Next you will see an "expected an indented block" error. ')
    #     # Retry again with fixed code
    #     new_code = "["  # This code will break upon execution, and it will be caught by the except clause
    #     result = run_program((new_code,index, image, query), queues_in_, input_type_,
    #                          retrying=True)[0]

    # # The function run_{sample_id} is defined globally (exec doesn't work locally). A cleaner alternative would be to
    # # save it in a global dict (replace globals() for dict_name in exec), but then it doesn't detect the imported
    # # libraries for some reason. Because defining it globally is not ideal, we just delete it after running it.
    # if f'execute_command_{sample_id}' in globals():
    #     del globals()[f'execute_command_{sample_id}']  # If it failed to compile the code, it won't be defined
    console.print(return_dict['answer'])
    return return_dict['answer']


def worker_init(queue_results_):
    global queue_results
    index_queue = mp.current_process()._identity[0] % len(queue_results_)
    queue_results = queue_results_[index_queue]


def main():
    #mp.set_start_method('spawn')

    #from vision_processes import queues_in, finish_all_consumers, forward, manager


    batch_size = config.dataset.batch_size
    num_processes = min(batch_size, 50)

    # if config.multiprocessing:
    #     queue_results_main = manager.Queue()
    #     queues_results = [manager.Queue() for _ in range(batch_size)]
    # else:
    #     queue_results_main = None
    #     queues_results = [None for _ in range(batch_size)]
    # #code = forward('codex', prompt=query, input_type="image")
    # queue_results_main = None
    # queues_results = [None for _ in range(batch_size)]
    # codex = partial(forward, model_name='codex', queues=[queues_in, queue_results_main])
    # #pdb.set_trace()
    # if config.clear_cache:
    #     cache.clear()

    # if config.wandb:
    #     import wandb
    #     wandb.init(project="viper", config=OmegaConf.to_container(config))
    #     # log the prompt file
    #     wandb.save(config.prompt)

    dataset = MyDataset(**config.dataset)

    with open(config.prompt) as f:
        base_prompt = f.read().strip()

    codes_all = None
    if config.use_cached_codex:
        results = pd.read_csv(config.cached_codex_path)
        codes_all = [r.split('# Answer is:')[1] for r in results['code']]
    # # python -c "from joblib import Memory; cache = Memory('cache/', verbose=0); cache.clear()"
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=True,
                            collate_fn=my_collate)
    input_type = dataset.input_type

    all_results = []
    all_answers = []
    all_codes = []
    all_ids = []
    all_querys = []
    all_img_paths = []
    all_possible_answers = []
    all_query_types = []
    code_dict = {}
    
    n_batches = len(dataloader)
    console.print('n batches')
    codex= CodexModel()
    for i, batch in tqdm(enumerate(dataloader), total=n_batches):
        console.print(batch,'batch')
        console.print(f'entry: {i}')
        #console.print(batch.keys())
        # Combine all querys and get Codex predictions for them
        # TODO compute Codex for next batch as current batch is being processed
        if not config.use_cached_codex:
            codes = codex(prompt=batch['query'], base_prompt=base_prompt)
            # console.print(len(codes),'num codes in main batch')
            # console.print(type(codes),'code type')
            if type(codes) != list:
                #console.print('I am executing something I should not')
                codes = [codes]

        else:
            codes = codes_all[i * batch_size:(i + 1) * batch_size]  # If cache

        # Run the code
        if config.execute_code:
                results = []
                for c, index, image_path,image, query,image_id in zip(codes,batch['index'],batch["sample_path"],batch['image'],batch['query'],batch["id"]):
                    code_dict[index] = c
                    console.print(image_path,'image path')
                    result = run_program([c,image_path,image_id,query],'',input_type)
                    results.append(result)
            
    # with mp.Pool(processes=num_processes, initializer=worker_init, initargs=(queues_results,)) \
    #         if config.multiprocessing else open(os.devnull, "w") as pool:
    #     try:
    #         n_batches = len(dataloader)
    #         for i, batch in tqdm(enumerate(dataloader), total=n_batches):
    #             console.print(batch,'batch')
    #             console.print(f'entry: {i}')
    #             #console.print(batch.keys())
    #             # Combine all querys and get Codex predictions for them
    #             # TODO compute Codex for next batch as current batch is being processed
    #             if not config.use_cached_codex:
    #                 codes = codex(prompt=batch['query'], base_prompt=base_prompt)
    #                 # console.print(len(codes),'num codes in main batch')
    #                 # console.print(type(codes),'code type')
    #                 if type(codes) != list:
    #                     #console.print('I am executing something I should not')
    #                     codes = [codes]
            
    #             else:
    #                 codes = codes_all[i * batch_size:(i + 1) * batch_size]  # If cache

    #             # Run the code
    #             if config.execute_code:
    #                     results = []
    #                     for c, index, image_path,image, query,image_id in zip(codes,batch['index'],batch["sample_path"],batch['image'],batch['query'],batch["id"]):
    #                         code_dict[index] = c
    #                         console.print(image_path,'image path')
    #                         result = run_program([c,image_path,image_id,query],queues_in,input_type)
    #                     # for c, sample_id, img, possible_answers, query in \
    #                     #         zip(codes, batch['sample_id'], batch['img'], batch['possible_answers'], batch['query']):
    #                     #     result = run_program([c, sample_id, img, possible_answers, query], queues_in, input_type)
    #                         results.append(result)
    #                 # if not config.multiprocessing:
    #                 #     # Otherwise, we would create a new model for every process
    #                 #     results = []
    #                 #     for c, index, image_path,image, query,image_id in zip(codes,batch['index'],batch["sample_path"],batch['image'],batch['query'],batch["id"]):
    #                 #         code_dict[index] = c
    #                 #         console.print(image_path,'image path')
    #                 #         result = run_program([c,image_path,image_id,query])
    #                 #     # for c, sample_id, img, possible_answers, query in \
    #                 #     #         zip(codes, batch['sample_id'], batch['img'], batch['possible_answers'], batch['query']):
    #                 #     #     result = run_program([c, sample_id, img, possible_answers, query], queues_in, input_type)
    #                 #         results.append(result)
    #                 # else:
    #                 #     results = list(pool.imap(partial(
    #                 #         run_program, queues_in_=queues_in, input_type_=input_type),
    #                 #         zip(codes, batch['sample_path'], batch['id'], batch['query'])))
    #             else:
    #                 p = 0
    #                 results = [(None, c) for c in codes]
    #                 #console.print(len(results),'num results')
    #                 for i in range(len(batch['index'])):
    #                     # console.print(i,'i')
    #                     # console.print(batch['index'][i])
    #                     index = batch['index'][i]
    #                     # print(len(codes),'codes')
    #                     c = results[i][1]
    #                     code_dict[index] = c
    #                 # for c, index, img, query in zip(codes,batch['index'],batch['image'],batch['query']):
    #                 #    p+= 1
    #                 #    console.print(f'{index},index')
    #                 #    console.print(f'p index {p}')
    #                 #    code_dict[index] = c
    #                 #console.print(results)
    #                 warnings.warn("Not executing code! This is only generating the code. We set the flag "
    #                               "'execute_code' to False by default, because executing code generated by a language "
    #                               "model can be dangerous. Set the flag 'execute_code' to True if you want to execute "
    #                               "it.")

    #             all_results += [r[0] for r in results]
    #             all_codes += [r[1] for r in results]
              
    #             # all_ids += batch['sample_id']
    #             all_answers += batch['answer']
    #             # all_possible_answers += batch['possible_answers']
    #             # all_query_types += batch['query_type']
    #             all_querys += batch['query']
    #             all_img_paths = []
    #             #all_img_paths += [dataset.get_img_path(idx) for idx in batch['index']]
    #             if i % config.log_every == 0:
    #                 try:
    #                     accuracy = datasets.accuracy(all_results, all_answers, all_possible_answers, all_query_types)
    #                     console.print(f'Accuracy at Batch {i}/{n_batches}: {accuracy}')
    #                 except Exception as e:
    #                     console.print(f'Error computing accuracy: {e}')

    #     except Exception as e:
    #         console.print(f'Exception: {e}')
    #         console.print("Completing logging and exiting...")

    # try:
    #     accuracy = datasets.accuracy(all_results, all_answers, all_possible_answers, all_query_types)
    #     console.print(f'Final accuracy: {accuracy}')
    # except Exception as e:
    #     print(f'Error computing accuracy: {e}')

    if config.save:
        results_dir = pathlib.Path(config['results_dir'])
        results_dir = results_dir / config.dataset.split
        results_dir.mkdir(parents=True, exist_ok=True)
        if not config.save_new_results:
            filename = 'results.csv'
        else:
            existing_files = list(results_dir.glob('results_*.csv'))
            if len(existing_files) == 0:
                filename = 'results_0.csv'
            else:
                filename = 'results_' + str(max([int(ef.stem.split('_')[-1]) for ef in existing_files if
                                                 str.isnumeric(ef.stem.split('_')[-1])]) + 1) + '.csv'
        print('Saving results to', filename)
        df = pd.DataFrame([all_results, all_answers, all_codes, all_ids, all_querys, all_img_paths,
                           all_possible_answers]).T
        df.columns = ['result', 'answer', 'code', 'id', 'query', 'img_path', 'possible_answers']
        # make the result column a string
        df['result'] = df['result'].apply(str)
        df.to_csv(results_dir / filename, header=True, index=False, encoding='utf-8')
        # torch.save([all_results, all_answers, all_codes, all_ids, all_querys, all_img_paths], results_dir/filename)
        with open('/home/michal5/viper/results/code_dict.json','w+') as f:
            json.dump(code_dict,f,indent=2)
        if config.wandb:
            wandb.log({'accuracy': accuracy})
            wandb.log({'results': wandb.Table(dataframe=df, allow_mixed_types=True)})

    finish_all_consumers()


if __name__ == '__main__':
    sys.stdout.write('hello')
    main()
