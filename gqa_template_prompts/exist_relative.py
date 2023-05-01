import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch


def exist_relative(image,main_object,second_object,relation):
    image_patch = ImagePatch(image)
    main_object_patch = image_patch.find_center(main_object)
    second_object_patch = image_patch.find_center(second_object)
    question = image_patch.location_template_relate(main_object,second_object,main_object_patch.center,second_object_patch.center,relation,image_patch.height,image_patch.width)
    answer = image_patch.llm_query(question,long_answer=True)
    if 'yes' in answer.lower()  or relation in answer.lower():
        return 'yes' 
    return 'no' 

