from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_97_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    if image_patch.exists("fish") and not image_patch.exists("bait"):
        return image_patch.llm_query("Is this a photo of they are using no bait but still got fish?")
    else:
        return "No, this is not a photo of them using no bait but still getting fish."
answer = execute_command(image)