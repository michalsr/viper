from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_13_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    caterpillar_patches = image_patch.find("caterpillar")
    plant_patches = image_patch.find("plants")
    if len(caterpillar_patches) > 0 and len(plant_patches) > 0:
        return "yes"
    else:
        return image_patch.llm_query("What is in this photo?")
answer = execute_command(image)