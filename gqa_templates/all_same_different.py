import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch


def check_all_same_different(image,obj,attribute,same=False):
    image_patch = ImagePatch(image)
    all_objs = image_patch.find_all(obj,k=5)
    all_properties = []
    for obj_patch in all_objs:
        all_properties.append(obj_patch.simple_query(f'Is {obj} {attribute}? Answer:'))
    if same:
        answer = all_properties[-1]
        if all(x==answer for x in all_properties):
            return 'yes'
    if not same:
        answer = all_properties[-1]
        if not all(x==answer for x in all_properties):
            return 'yes'
    return 'no'
