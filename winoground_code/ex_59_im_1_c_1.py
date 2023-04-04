from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_59_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    banana_patches = image_patch.find("banana")
    apple_patches = image_patch.find("apple")
    if len(banana_patches) == 2 and len(apple_patches) == 3:
        return "yes"
    else:
        return "no"
answer = execute_command(image)