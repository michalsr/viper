import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch

def verify_global(image,attribute_1,attribute_2=None,object_name=None):
    image_patch = ImagePatch(image)
    if object_name == None:
        object_name = 'scene'
    if attribute_2 == None:
        score = image_patch.verify_property(object_name,attribute_1)
        if score > 0.6:
            return 'yes'
    else:
        score_1 = image_patch.verify_property(object_name,attribute_1)
        score_2 = image_patch.verify_property(object_name,attribute_2)
        if score_1 > 0.6 and score_2>0.6:
            return 'yes'
    return 'no' 