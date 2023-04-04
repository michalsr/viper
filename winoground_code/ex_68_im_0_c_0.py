from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_68_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    return image_patch.llm_query("Is this a photo of it ran away while they pursued?", long_answer=False)
answer = execute_command(image)