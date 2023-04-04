from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_16_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    forks = len(image_patch.find("fork"))
    spoons = len(image_patch.find("spoon"))
    if forks < spoons:
        return "yes"
    elif forks > spoons:
        return "no"
    else:
        return image_patch.llm_query("Are there fewer forks than spoons in this image?")
answer = execute_command(image)