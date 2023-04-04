from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_94_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    return image_patch.llm_query("Is this a photo of The dog rides without a visible tongue?")
answer = execute_command(image)