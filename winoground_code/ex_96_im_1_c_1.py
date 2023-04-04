from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_96_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    if image_patch.exists("leaves"):
        return image_patch.llm_query("Is this a photo of shedding its leaves?")
    else:
        return "No leaves found in the image."
answer = execute_command(image)