from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_15_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    snowboarder_patches = image_patch.find("snowboarder")
    skier_patches = image_patch.find("skier")
    if len(snowboarder_patches) > len(skier_patches):
        return "yes"
    elif len(snowboarder_patches) < len(skier_patches):
        return "no"
    else:
        return image_patch.llm_query("Are there more snowboarders or skiers in this location?")
answer = execute_command(image)