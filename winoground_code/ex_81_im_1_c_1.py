from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_81_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    left_hand_patches = image_patch.find("left hand")
    right_hand_patches = image_patch.find("right hand")
    passport_patches = image_patch.find("passport")
    suitcase_patches = image_patch.find("suitcase handle")
    
    if len(left_hand_patches) == 0 or len(right_hand_patches) == 0 or len(passport_patches) == 0 or len(suitcase_patches) == 0:
        return "no"
    
    left_hand_patch = left_hand_patches[0]
    right_hand_patch = right_hand_patches[0]
    passport_patch = passport_patches[0]
    suitcase_patch = suitcase_patches[0]
    
    if left_hand_patch.horizontal_center < passport_patch.horizontal_center and right_hand_patch.horizontal_center > suitcase_patch.horizontal_center:
        return "yes"
    else:
        return "no"
answer = execute_command(image)