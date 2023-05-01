import os
import json
import subprocess

import numpy as np

from PIL import Image
from tqdm import tqdm
from torch.utils.data import Dataset

ROOT_DIR='/home/michal5/data/'
class GQA(Dataset):
    def __init__(self, annotation_file='train',root_dir=ROOT_DIR):
        self.root_dir = root_dir
        if annotation_file == 'train':
            file_to_open =ROOT_DIR+ 'gqa/train_all_question/train_all_questions_0.json'
            
        elif annotation_file == 'val':
            file_to_open = ROOT_DIR+'gqa/val_all_questions.json'
        else:
            file_to_open = ROOT_DIR+'gqa/testdev_all_questions.json'
        with open(file_to_open) as f:
            self.annotations = json.load(f)
    def __len__(self):
        return len(self.annotations)
    def __getitem__(self, index):
        entry = self.annotations[index]
        image_id = entry['imageId']
        question = entry['question']
        image_path = ROOT_DIR+f'gqa/images/{image_id}.jpg'
        image = Image.open(image_path).convert('RGB')
        answer = entry['answer']
        out_dict = {"id":str(index),"sample_path":image_path,"query":question, "answer": answer, "image": image, 'index': index,'sample_id':index,'possible_answers':['hi'],'query_type':'question'}
        return out_dict

        