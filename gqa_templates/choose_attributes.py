import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch

def choose_attribute(image,object_name,attribute_1,attribute_2):
    image_patch = ImagePatch(image)
    selected_object = image_patch.find_center(object_name)
    score_1 = selected_object.verify_property(object_name,attribute_1)
    score_2 = selected_object.verify_property(object_name,attribute_2)
    if score_1 > score_2:
        return attribute_1
    else:
        return attribute_2