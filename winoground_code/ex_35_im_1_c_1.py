from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_35_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    rectangular_sign_patches = image_patch.find("rectangular sign")
    circular_sign_patches = image_patch.find("circular sign")
    if len(rectangular_sign_patches) == 0 or len(circular_sign_patches) == 0:
        return "no"
    rectangular_sign_patches.sort(key=lambda x: x.vertical_center)
    circular_sign_patches.sort(key=lambda x: x.vertical_center)
    if rectangular_sign_patches[0].upper < circular_sign_patches[0].lower:
        return "yes"
    else:
        return "no"
answer = execute_command(image)