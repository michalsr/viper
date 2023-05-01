import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch

def choose_global(image,attribute_1,attribute_2,object_name=None):
    image_patch = ImagePatch(image)
    if object_name == None:
        obj_name = 'scene'
    else:
        obj_name = object_name
    score_1 = image_patch.verify_property(obj_name,attribute_1)
    score_2 = image_patch.verify_property(obj_name,attribute_2)
    if score_1 > score_2:
        return attribute_1
    else:
        return attribute_2