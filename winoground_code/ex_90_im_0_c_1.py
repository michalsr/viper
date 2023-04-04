from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_90_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    wheel_patches = image_patch.find("wheel")
    human_patches = image_patch.find("human")
    if len(wheel_patches) == 2 and len(human_patches) == 1:
        return "yes"
    else:
        return image_patch.llm_query("Is this a photo of two wheels and one human?")
answer = execute_command(image)