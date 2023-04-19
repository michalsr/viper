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
from datasets.dataset import MyDataset
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

    

    c,image_path,example_id,query = parameters

    file_path = f'/home/michal5/viper/winoground_code_number_v6/{example_id}.py'

    console.print(example_id,'example id')

    code_header = f"from image_patch import ImagePatch\nimport numpy as np\nfrom image_patch import distance\nfrom image_patch import avg\nfrom PIL import Image\nimage = Image.open('{image_path}').convert('RGB')\n"
    code_end = f"answer = execute_command(image)"
    all_code = code_header+c+'\n'+code_end
    with open(file_path,'w+') as f:
        f.write(all_code)
    # bad_examples = ['ex_37_im_1_c_1','ex_38','ex_150','ex_39','ex_40','ex_41','ex_47','ex_55','ex_66','ex_77']
    # return_dict = {}
    # for b in bad_examples:
    #     if b in example_id:
    #         return_dict['answer'] = 'Broken'
    #         return return_dict
    return_dict = {}
    

    exec(all_code,globals(),return_dict)
    return return_dict['answer']
def main():
    #  batch_size = config.dataset.batch_size
    #  #console.print('hello i am here')
    #  dataset = MyDataset(**config.dataset)
    #  with open(config.prompt) as f:
    #     base_prompt = f.read().strip()
    #  dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=True,
    #                         collate_fn=my_collate)
    #  input_type = dataset.input_type

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
     files_to_run = os.listdir('/home/michal5/viper/winoground_code_number_v5')
     for f in files_to_run:
        with open(f'/home/michal5/viper/winoground_code_number_v5/'+f) as c:
             try:
                return_dict = {}
                exec(c.read(),globals(),return_dict)
                results_dict[f] = return_dict['answer']
             except:
                results_dict[f] = 'error'
     
    #  n_batches = len(dataloader)
     #console.print('n batches')
    #  for i, batch in tqdm(enumerate(dataloader), total=n_batches):
    #     codes = forward('codex', prompt=batch['query'],base_prompt=base_prompt, input_type="image")
    #     if type(codes) != list:
    #         codes = [codes]
    #     results = []
    #     for c, index, image_path,image, query,example_id in zip(codes,batch['index'],batch["sample_path"],batch['image'],batch['query'],batch["id"]):
    #         code_dict[index] = c
    #         #console.print(image_path,'image path')
    #         # result = run_program([c,image_path,example_id,query],'',input_type)
    #         # results.append(result)
    #         # results_dict[example_id] = result
    #         try:
    #             result = run_program([c,image_path,example_id,query],'',input_type)
    #             results.append(result)
    #             results_dict[example_id] = result
    #         except:
    #             #sprint(run_program([c,image_path,example_id,query],'',input_type))
    #             results_dict[example_id] = 'error'
    #             continue  
     new_results_dict = {}
     for r in results_dict:
        entry = results_dict[r]
        if torch.is_tensor(entry):
            new_results_dict[r] = entry.item()
        else:
            new_results_dict[r] = entry
     with open('/home/michal5/viper/winoground_test.json','w+') as f:
        json.dump(new_results_dict,f)
         
     finish_all_consumers()



    


if __name__ == '__main__':
    sys.stdout.write('hello')
    main()
