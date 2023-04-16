import torch 
from transformers import DetrForObjectDetection
from transformers import ConditionalDetrConfig, ConditionalDetrModel
from PIL import Image
import json
print('hi')
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
from torch.utils.data import Dataset
from PIL import Image
print('hi 2')
class COCO_Dataset(Dataset):
    def __init__(self,transform=None,target_transform=None):
        with open('/data/michal5/annotations/instances_train2014.json','r+') as f:
            self.annotations = json.load(f)
        self.image_dir = '/data/michal5/coco/images'
        self.class_names = class_names 
    def __len__(self):
        return len(self.annotations['annotations'])
    def __getitem__(self,idx):
        entry = self.annotations['annotations'][idx]
        print(entry,'entry')
        class_id = entry['category_id']
        bbox = entry['bbox']
        image_id = entry['image_id']
        full_id = 'COCO_train2014_'+str(entry['image_id']).zfill(12)
        full_image_path = f'/data/michal5/coco/images/train2014/{full_id}.jpg'
        image = Image.open(full_image_path).convert('RGB')
        target = {'image_id': image_id,'category_id':entry['category_id'],'bbox':bbox,'class_name':self.class_names[class_id]}
        return image,target 
import json
from torch.utils.data import DataLoader
dataset = COCO_Dataset()
from transformers import AutoImageProcessor, DeformableDetrForObjectDetection
from transformers import AutoImageProcessor, AutoModelForObjectDetection,  OwlViTForObjectDetection
from transformers import OwlViTProcessor
print('hi 3')
# get processor and models based on action 
# 0 = deformable detr 
# 1 = conditional detr
# 2 = owl vit 
deformable_detr= {"image_processing":AutoImageProcessor.from_pretrained("SenseTime/deformable-detr"),"model":DeformableDetrForObjectDetection.from_pretrained("SenseTime/deformable-detr")}
conditional_detr = {"image_processing":AutoImageProcessor.from_pretrained("microsoft/conditional-detr-resnet-50"),
                   "model":AutoModelForObjectDetection.from_pretrained("microsoft/conditional-detr-resnet-50")}
owl_vit = {"image_processing": OwlViTProcessor.from_pretrained("google/owlvit-base-patch32"),"model":OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32")}

processor_model_dict = {0:deformable_detr,1:conditional_detr,2:owl_vit}
test_sample = dataset[0]
print(test_sample)
import sys
sys.path.append('/shared/rsaas/michal5/viper')
from pycocotools.coco import COCO

from coco_eval import CocoEvaluator
coco_gt = COCO('/data/michal5/annotations/instances_train2014.json')
evaluator = CocoEvaluator(coco_gt,['bbox'])
print('hi 4')