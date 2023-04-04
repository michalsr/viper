from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_45_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    drink_patches = image_patch.find("drink")
    if len(drink_patches) == 0:
        return "no"
    drink_patch = drink_patches[0]
    if drink_patch.verify_property("drink", "cold"):
        if image_patch.verify_property("image", "hot day"):
            return "yes"
    return "no"
answer = execute_command(image)