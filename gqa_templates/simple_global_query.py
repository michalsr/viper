import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch

def query_global(image,caption):
    # send to qa model 
    image_patch = ImagePatch(image)
    answer = image_patch.simple_query(caption)
    return answer 