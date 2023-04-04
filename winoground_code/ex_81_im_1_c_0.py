from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_81_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    suitcase_patches = image_patch.find("suitcase")
    passport_patches = image_patch.find("passport")
    if len(suitcase_patches) == 0 or len(passport_patches) == 0:
        return "no"
    suitcase_patch = suitcase_patches[0]
    passport_patch = passport_patches[0]
    if suitcase_patch.left < passport_patch.left:
        return "no"
    if suitcase_patch.lower > passport_patch.lower:
        return "no"
    if suitcase_patch.upper < passport_patch.upper:
        return "no"
    if suitcase_patch.horizontal_center < passport_patch.horizontal_center:
        return "no"
    return "yes"
answer = execute_command(image)