import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch
from image_patch import compare_relation
def multi_obj_rel(image,obj_list=[],obj_relation_list=[]):
    verify_obj_relation_list = []
    answer = None 
    image_patch = ImagePatch(image)
    obj_dict = {}
    for obj in obj_list:
        obj_dict[obj] = image_patch.find_all(obj,k=5)
    for i,entry in enumerate(reversed(obj_relation_list)):
        object_1, relation, object_2 = entry
        positive_entries_obj_1 = [] 
        positive_entries_obj_2 = []
        for obj_1_patch in obj_dict[object_1]:
            for obj_2_patch in obj_dict[object_2]:
                answer = compare_relation(obj_1_patch.center,obj_2_patch.center,relation,rel_2=None)
                
                
                if 'no' not in answer.lower():
                    verify_obj_relation_list.append('yes')
                    positive_entries_obj_1.append(obj_1_patch)
                    positive_entries_obj_2.append(obj_2_patch)
        if len(positive_entries_obj_2) != 0:
            obj_dict[object_2]= positive_entries_obj_2
        else:
            return 'no'
        if len(positive_entries_obj_1) != 0:
            obj_dict[object_1] = positive_entries_obj_1
        else:
            return 'no'
        if len(verify_obj_relation_list)<  i+1:
            verify_obj_relation_list.append('no')
    if all(x == 'yes' for x in verify_obj_relation_list): 
        return 'yes'
    return 'no'
                    
                
