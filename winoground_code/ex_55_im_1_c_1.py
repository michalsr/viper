from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_55_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    green_patches = image_patch.find("green")
    blue_patches = image_patch.find("blue")
    green_patch = green_patches[0]
    blue_patch = blue_patches[0]
    if green_patch.width > blue_patch.width and green_patch.height > blue_patch.height:
        return bool_to_yesno(True)
    elif blue_patch.width > green_patch.width and blue_patch.height > green_patch.height:
        return bool_to_yesno(True)
    else:
        return bool_to_yesno(False)
answer = execute_command(image)