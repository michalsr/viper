import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch

def choose_object(image,option_1,option_2):
    image_patch = ImagePatch(image)
    object_1_patch = image_patch.find_center(option_1)
    object_2_patch = image_patch.find_center(option_2)
    if object_1_patch.score > object_2_patch.score:
        return option_1
    return option_2 