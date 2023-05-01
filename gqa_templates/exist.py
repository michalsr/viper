import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch

def exist(image,object_name_1,object_name_2=None,both=False):
    image_patch = ImagePatch(image)
    if object_name_2 == None:
        selected_object = image_patch.find_center(object_name_1)
        if selected_object.score >0.1:
            return 'yes' 
    else:
        selected_object_1 = image_patch.find_center(object_name_1)
        selected_object_2 = image_patch.find_center(object_name_2)
        if not both:
            if selected_object_1.score>0.1 or selected_object_2.score>0.1:
                return 'yes'
        else:
            if selected_object_1.score>0.1 and selected_object_2.score>0.1:
                return 'yes'
    return 'no'
