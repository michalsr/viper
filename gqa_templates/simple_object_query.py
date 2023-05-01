import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch
def query_object(image,object_name,question):
    image_patch = ImagePatch(image)
    object_patch = image_patch.find_center(object_name)
    answer = object_patch.simple_query(question)
    return answer 
