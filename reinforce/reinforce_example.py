import sys
import torch 
from transformers import DetrForObjectDetection
from transformers import ConditionalDetrConfig, ConditionalDetrModel
from PIL import Image
from torch.utils.data import Dataset
import json
from torchvision import transforms
from transformers import AutoImageProcessor, DeformableDetrForObjectDetection
from transformers import AutoImageProcessor, AutoModelForObjectDetection,  OwlViTForObjectDetection
from transformers import OwlViTProcessor
import torch.optim as optim
from pycocotools.coco import COCO
import torch.nn.functional as F
sys.path.append('/home/michal5/viper')
from coco_eval import CocoEvaluator
from torch.distributions import Categorical
import numpy as np
import torch.nn as nn  
from tqdm import tqdm 
class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()
        self.affine1 = nn.Linear(91, 128)
        self.dropout = nn.Dropout(p=0.6)
        self.affine2 = nn.Linear(128, 3)

        self.saved_log_probs = []
        self.rewards = []

    def forward(self, x):
        x = self.affine1(x)
        x = self.dropout(x)
        x = F.relu(x)
        action_scores = self.affine2(x)
        return F.softmax(action_scores, dim=1)
policy = Policy()
optimizer = optim.Adam(policy.parameters(), lr=1e-2)
coco_gt = COCO('/data/michal5/coco/annotations/instances_train2017.json')
evaluator = CocoEvaluator(coco_gt,['bbox'])
class_names = ['person','bicycle','car','motorcycle','airplane',
              'bus','train','truck','boat','traffic light','fire hydrant',
              'street sign','stop sign','parking meter','bench',
              'bird','cat','dog','horse','sheep','cow','elephant',
              'bear','zebra','giraffe','hat','backpack','umbrella',
              'shoe','eye glasses','handbag','tie','suitcase',
              'frisbee','skis','snowboard','sports ball','kite',
              'baseball bat','baseball glove','skateboard',
              'surfboard','tennis racket','bottle','plate',
              'wine glass','cup','fork','knife','spoon','bowl',
              'banana','apple','sandwich','orange','broccoli',
              'carrot','hot dog','pizza','donut','cake','chair','couch',
              'potted plant','bed','mirror','dining table','window',
              'desk','toilet','door','tv','laptop','mouse','remote',
              'keyboard','cell phone','microwave','oven',
              'toaster','sink','refrigerator','blender','book',
              'clock','vase','scissors','teddy bear','hair drier',
              'toothbrush','hair brush']
deformable_detr= {"image_processing":AutoImageProcessor.from_pretrained("SenseTime/deformable-detr"),"model":DeformableDetrForObjectDetection.from_pretrained("SenseTime/deformable-detr")}
conditional_detr = {"image_processing":AutoImageProcessor.from_pretrained("microsoft/conditional-detr-resnet-50"),
                   "model":AutoModelForObjectDetection.from_pretrained("microsoft/conditional-detr-resnet-50")}
owl_vit = {"image_processing": OwlViTProcessor.from_pretrained("google/owlvit-base-patch32"),"model":OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32")}
# policy = Policy()
# print(policy,'policy')
processor_model_dict = {0:deformable_detr,1:conditional_detr,2:owl_vit}
def convert_to_one_hot(class_name):
    index = class_names.index(class_name)
    all_zeros = torch.zeros(len(class_names))
    all_zeros[index] = 1.0
    return all_zeros

def get_action(class_name):
    device = 'cuda'
    new_inputs = []
    one_hot = convert_to_one_hot(category)
    probs = policy(new_inputs)
    m = Categorical(probs)
    action = m.sample()
    policy.saved_log_probs.append(m.log_prob(action))
    return action 

   
# def get_action(class_name):
#     device = 'cuda'
#     new_inputs = []
#     for i in inputs:
#         image, target = i
#         category = target['class_name']
#         one_hot = convert_to_one_hot(category)
#         new_inputs.append(one_hot)
#     new_inputs =torch.stack(new_inputs)
#     #new_inputs = new_inputs.to(device)
#     probs = policy(new_inputs)
#     m = Categorical(probs)
#     action = m.sample()

#     policy.saved_log_probs.append(m.log_prob(action))
#     return action
class COCO_Dataset(Dataset):
    def __init__(self,transform=None,target_transform=None):
        with open('/data/michal5/coco/annotations/instances_train2017.json','r+') as f:
            self.annotations = json.load(f)
        self.image_dir = '/data/michal5/coco/images'
        self.class_names = class_names 
        self.idx_to_actions = idx_to_actions
    def get_actions(self):
        idx_to_actions = {}
        for i in range(len(self.annotations['annotations'])):
            entry = self.annotations['annotations'][i]
            action = get_action(self.class_names[entry['category_id']])
            idx_to_actions[i] = action.item()
        return idx_to_actions
    def __len__(self):
        return len(self.annotations['annotations'])
    def __getitem__(self,idx):
        entry = self.annotations['annotations'][idx]
        class_id = entry['category_id']
        bbox = entry['bbox']
        image_id = entry['image_id']
        class_name = self.class_names[class_id]
        action = get_action(self.class_names[class_id])
        full_id = str(entry['image_id']).zfill(12)
        full_image_path = f'/data/michal5/coco/images/train2017/{full_id}.jpg'
        image = Image.open(full_image_path).convert('RGB')
        if action.item() != 2:
            encoding = processor_model_dict["image_processing"](images=image,return_tensors="pt")
        else:
            text = [[f'a photo of {class_name}']]
            encoding = processor_model_dict["image_processing"](images=image,text=text,return_tensors="pt")
        target = {'action':action,'image_id': image_id,'category_id':entry['category_id'],'bbox':bbox,'class_name':self.class_names[class_id]}
        return encoding,target 





def sort_by_action(batches,actions):
    action_dict = {}
    for batch,action in zip(batches,actions):
        if action.item() not in action_dict:
            action_dict[action.item()] = []
        action_dict[action.item()].append(batch)
    return action_dict 

def collate_fn(batch,processor,action):
    
    image = [item[0] for item in batch]
    original_size = [torch.tensor(img.size[::-1]) for img in image]
    if action != 2:
        inputs = processor(images=image,return_tensors="pt")
    else:
         class_name = [item[1]['class_name'] for item in batch]
         text = ['a photo of a ' + t for t in class_name]
         inputs = processor(images=image,text=text,return_tensors="pt")


    category = [item[1]['category_id'] for item in batch]
    bbox = [item[1]['bbox'] for item in batch]
    class_name = [item[1]['class_name'] for item in batch]
    image_id = [item[1]['image_id'] for item in batch]
    original_size = torch.stack(original_size)
    batch = {}

    batch['category'] = category
    batch['bbox'] = bbox
    batch['class_name'] = class_name
    batch['image_id'] = image_id 
    return inputs, batch, original_size


# get processor and models based on action 
# 0 = deformable detr 
# 1 = conditional detr
# 2 = owl vit 





def run_detection(action_dict):

    for entry in action_dict:
        action = entry
        batch = action_dict[action]
        processor_model = processor_model_dict[action]
        processor_model["model"] = processor_model["model"].to('cuda')
        processor_model["model"].eval()
        inputs,target,target_sizes = collate_fn(batch,processor_model["image_processing"],action)

        # text = [target['class_name']]
        # text = ['a photo of a ' + t for t in text]
        # if action != 2:
        #     inputs = processor_model["image_processing"](images=image,return_tensors="pt")
        # else:
        #     text_input = [[f'a photo of a {target}']]
        #     inputs = processor_model["image_processing"](text=text, images=image, return_tensors="pt")
        inputs = {k:v.to('cuda') for k,v in inputs.items()}
        with torch.no_grad():
            output = processor_model["model"](**inputs)
            output.logits = output.logits.to('cpu')
            output.pred_boxes = output.pred_boxes.to('cpu')
            #output = {k:v.to('cpu') for k,v in output.items()}
            results = processor_model["image_processing"].post_process_object_detection(outputs=output, threshold=0.1, target_sizes=target_sizes)
            result = results[0]
            inputs = {k:v.to('cpu') for k,v in inputs.items()}
            res = {targ: output for targ, output in zip(target['image_id'],results)}
            processor_model["model"] = processor_model["model"].to('cpu')
            torch.cuda.empty_cache()

            evaluator.update(res)
    evaluator.synchronize_between_processes()
    evaluator.accumulate()
    answer = evaluator.summarize()
    evaluator.img_ids = []
    evaluator.eval_imgs = {'bbox':[]}
    return answer
    
def finish_episode():
    R = 0
    policy_loss = []
    returns = deque()
    for r in policy.rewards[::-1]:
        R = r + gamma*R
        returns.appendleft(R)
    returns = torch.tensor(returns)
    returns = (returns - returns.mean()) / (returns.std() + eps)
    for log_prob, R in zip(policy.saved_log_probs, returns):
        policy_loss.append(-log_prob * R)
    optimizer.zero_grad()
    policy_loss = torch.cat(policy_loss).sum()
    policy_loss.backward()
    optimizer.step()
    del policy.rewards[:]
    del policy.saved_log_probs[:]


def sort_by_action(idx_to_action):
    action_dict = {}
    for i in set(list(idx_to_action.values())):
        action_dict[i]= [k for k,v idx_to_action.items() if v==i]
    return action_dict 


def main(num_episodes):
    running_reward = 0 

    for ep in range(num_episodes):
        dataset = COCO_Dataset()
        episode_reward = 0 
        # find all actions 
        # for each action select subset based on indices
        # create collate fn based on processor for that 
        # create loader 
        # get rewards 
        for i in tqdm(range(0,len(dataset),32)):
            batches = [dataset[j] for j in range(i,i+32)]
            action = get_action(batches)
            action_dict = sort_by_action(batches,action)
            rewards = run_detection(action_dict)
            policy.rewards.append(np.mean(rewards))
            episode_reward += np.mean(rewards)
        
        running_reward = 0.05 * ep_reward + (1 - 0.05) * running_reward
        finish_episode()
        if i % 2 == 0:
            print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'.format(
                  i, episode_reward, running_reward))
        

if __name__ == '__main__':
    main(1)

       




