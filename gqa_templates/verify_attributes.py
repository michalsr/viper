import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch

def verify_attribute(image,object_1,attribute_1,attribute_2=None,object_2=None,both=False):
    image_patch = ImagePatch(image)
    selected_object_1 = image_patch.find_center(object_1)
    score_1 = selected_object_1.verify_property(object_1,attribute_1)
    if attribute_2 == None and object_2 == None:
        if score_1 > 0.6:
            return 'yes'
    if attribute_2 != None and object_2 == None:
        score_2 = selected_object_1.verify_property(object_1,attribute_2)
        # if both:
        #     if score_1>0.6 and score_2>0.6:
        #         return 'yes'
        # else:
        #     if score_1>0.6 or score_2>0.6:
        #         return 'yes'
    if object_2!= None and attribute_2 == None:
        selected_object_2 = image_patch.find_center(object_2)
        score_2 = selected_object_2.verify_property(object_2,attribute_1)

    if object_2 != None and attribute_2 != None:
        score_2 = selected_object_2.verify_property(object_2,attribute_2)
    if both:
        if score_1>0.6 and score_2>0.6:
            return 'yes'
        else:
            if score_1>0.6 or score_2>0.6:
                return 'yes'
    # # all 4
    # # obj_1, att_1, att_2
    # # obj_1, att_1, obj_2, or/and
    # # obj_1, att_1 
    # if attribute_2 != None and object_2 == None:
    #     score_2 = selected_object.verify_property(object_1,attribute_2)
    #     if score_1 > 0.6 and score_2>0.6:
    #         return 'yes' 
    # else:
    #     if score_1 > 0.6: 
    #         return 'yes'
    return 'no' 
