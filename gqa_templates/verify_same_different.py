import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch

def check_two_same_different(image,obj_1,obj_2,property,same=False):
    image_patch = ImagePatch(image)
    obj_1_patch = image_patch.find_center(obj_1)
    obj_2_patch = image_patch.find_center(obj_2)
    obj_1_property = obj_1_patch.simple_query(f'Question: What is the {property} of {obj_1}. Answer:')
    obj_2_property = obj_2_patch.simple_query(f'Question:What is the {property} of {obj_2}. Answer:')
    if same:
        if obj_1_property == obj_2_property:
            return 'yes' 
    if not same:
        if obj_1_property != obj_2_property:
            return 'yes' 
    return 'no'
    
