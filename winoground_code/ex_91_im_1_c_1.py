from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_91_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    if image_patch.exists("lines") and image_patch.exists("clothing"):
        return "yes"
    else:
        return image_patch.llm_query("Is this a photo of lines on clothing?")
answer = execute_command(image)