from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_39_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    helpful_patches = image_patch.find("helpful person")
    hurt_patches = image_patch.find("hurt person")
    helpful_patches.sort(key=lambda x: x.left)
    hurt_patches.sort(key=lambda x: x.left)
    if helpful_patches[0].left < hurt_patches[0].left:
        return "yes"
    else:
        return "no"
answer = execute_command(image)