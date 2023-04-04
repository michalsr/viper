from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_97_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    if image_patch.exists("bait") and not image_patch.exists("fish"):
        return "yes"
    else:
        return "no"
answer = execute_command(image)