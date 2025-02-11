# import ast
# import math
# import sys
# import time

# import requests
# import torch.multiprocessing as mp
# from joblib import Memory
# from rich.console import Console
# from rich.live import Live
# from rich.padding import Padding
# from rich.pretty import pprint
# from rich.prompt import Prompt
# from rich.syntax import Syntax
# from rich import print
# from rich.markup import escape as rich_escape

# from IPython.display import update_display, clear_output, display
# from PIL import Image
# import matplotlib.pyplot as plt

# from configs import config
# from utils import show_single_image
# from tqdm import tqdm 
# from IPython.display import update_display, clear_output
# from IPython.core.display import HTML

# cache = Memory('cache/' if config.use_cache else None, verbose=0)
from tqdm import tqdm
import os 
import json 
from main_simple_lib import *
from datasets.aro_dataset import VG_Relation
from torch.utils.data import DataLoader
from vision_processes import finish_all_consumers
def my_collate(batch):
    # Avoid stacking images (different size). Return everything as a list
    to_return = {k: [d[k] for d in batch] for k in batch[0].keys()}
    return to_return
def run_program(parameters, queues_in_, input_type_, retrying=False):
    from image_patch import ImagePatch, llm_query, best_image_match, distance, bool_to_yesno
    from video_segment import VideoSegment

    global queue_results

    

    c,image_path,example_id,query,answer = parameters



    #console.print(example_id,'example id')

    code_header = f"from image_patch import ImagePatch\nfrom image_patch import distance\nfrom image_patch import avg\nfrom PIL import Image\nimage = Image.open('{image_path}').convert('RGB')\n"
    code_end = f"answer = execute_command(image)"
    all_code = code_header+c+'\n'+code_end

    # bad_examples = ['ex_37_im_1_c_1','ex_38','ex_150','ex_39','ex_40','ex_41','ex_47','ex_55','ex_66','ex_77']
    # return_dict = {}
    # for b in bad_examples:
    #     if b in example_id:
    #         return_dict['answer'] = 'Broken'
    #         return return_dict
    return_dict = {}
    

    exec(all_code,globals(),return_dict)
    return return_dict['answer']
def write_code(code,example_id,image_path,incorrect):
    if incorrect:
        file_path = '/home/michal5/viper/vg_relation_code_incorrect'
    else:
        file_path = '/home/michal5/viper/vg_relation_code_execute'
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    code_header = f"from image_patch import ImagePatch\nfrom image_patch import distance\nfrom image_patch import avg\nfrom PIL import Image\nimage = Image.open('{image_path}').convert('RGB')\n"
    code_end = f"answer = execute_command(image)"
    all_code = code_header+code+'\n'+code_end
    full_file_path = file_path+f'/{example_id}.py'
    with open(full_file_path,'w+') as f:
        f.write(all_code)
    

def main():
     batch_size = config.dataset.batch_size
     #console.print('hello i am here')
     subset = list(range(config.dataset.start_sample,config.dataset.start_sample+config.dataset.max_samples))
     dataset = VG_Relation(image_preprocess=None)
     dataset = torch.utils.data.Subset(dataset,subset)
     with open(config.prompt) as f:
        base_prompt = f.read().strip()
     #print(base_prompt)
     dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=True,
                            collate_fn=my_collate)



     all_results = []
     all_answers = []
     all_codes = []
     all_ids = []
     all_querys = []
     all_img_paths = []
     all_possible_answers = []
     all_query_types = []
     code_dict = {}
     results_dict = {}
    
     n_batches = len(dataloader)
     num_questions = 0
     correct = 0
     total =0 
     errors = 0
     answered = 0
     #console.print('n batches')
     for i, batch in tqdm(enumerate(dataloader), total=n_batches):
            if  i!=0:
                #correct = sum(list(results_dict.values()))
                #total = len(list(results_dict.values()))
                print(f'Correct:{correct}')
                print(f'Total:{total}')
                print(f'Answered:{answered}')
                print(f'Errors:{errors}')
                #print(correct,total,errors,i)

            codes = forward('codex', prompt=batch['query'],base_prompt=base_prompt, input_type="image")
            if type(codes) != list:
                codes = [codes]
            results = []
            for c, index, image_path,image, query,example_id,answer in zip(codes,batch['index'],batch["sample_path"],batch['image'],batch['query'],batch["id"],batch['answer']):
                
                # code_dict[index] = c
                
                # #console.print(image_path,'image path')
                # print(c,'c')
                # result = run_program([c,image_path,example_id,query,answer],'',None)
                
                # print('result',result)
                # print('answer',answer)
                # if result == answer:
                #     results_dict[example_id] = 1
                # else:
                #     results_dict[example_id] = 0
                #     print('Wrong')
                total +=1
                print(c,'c')
                try:
                    result = run_program([c,image_path,example_id,query,answer],'',None)
                    answered +=1
                    print('result',result)
                    print('answer',answer)
                    if result == answer:
                        results_dict[example_id] = 1
                        correct += 1
                    else:
                        results_dict[example_id] = 0
                        print('Wrong')
                        #write_code(c,example_id,image_path,incorrect=True)
                
                    # results.append(result)
                    #results_dict[example_id] = result
                except:
                    #sprint(run_program([c,image_path,example_id,query],'',input_type))
                    results_dict[example_id] = 0
                    errors+=1
                    print('Error',query)
                    #write_code(c,example_id,image_path,incorrect=False)
                    continue 

     with open('/home/michal5/viper/aro_10000_11000.json','w+') as f:
         json.dump(results_dict,f)
         
     finish_all_consumers()



    


if __name__ == '__main__':
    sys.stdout.write('hello')
    main()
