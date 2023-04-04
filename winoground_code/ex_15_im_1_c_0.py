from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_15_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    skier_patches = image_patch.find("skier")
    snowboarder_patches = image_patch.find("snowboarder")
    if len(skier_patches) > len(snowboarder_patches):
        return "yes"
    elif len(skier_patches) < len(snowboarder_patches):
        return "no"
    else:
        return image_patch.llm_query("Are there more skiers or snowboarders in this photo?")
answer = execute_command(image)