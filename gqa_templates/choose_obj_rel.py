import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch

def choose_obj_rel(image,prefix,option_1,option_2):
    image_patch = ImagePatch(image)
    chosen_option = image_patch.best_text_match(prefix=prefix,option_list=[option_1,option_2])
    return chosen_option 
  
