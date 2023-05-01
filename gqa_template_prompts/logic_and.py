import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch

def logic_and(image,object_1,object_2):
     image_patch  = ImagePatch(image)
     object_1_patch = image_patch.find_center(object_1)
     object_2_patch = image_patch.find_center(object_2)
     if object_1_patch.score > 0.1 and object_2_patch.score > 0.1:
          return 'yes'
     return 'no'