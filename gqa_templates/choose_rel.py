import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch
from image_patch import compare_relation

def choose_rel(image,obj_1,obj_2,rel_1,rel_2=None):
    image_patch = ImagePatch(image)
    obj_1_patch = image_patch.find_center(obj_1)
    obj_2_patch = image_patch.find_center(obj_2)
    answer = compare_relation(obj_1_patch.center,obj_2_patch.center,rel_1,rel_2)
    if 'yes' in answer.lower():
        return 'yes'
    if 'no' in answer.lower():
        return 'no'
    return answer 
    
             



