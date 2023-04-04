from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_57_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    if image_patch.exists("person") and image_patch.exists("dough"):
        person_patch = image_patch.find("person")[0]
        dough_patch = image_patch.find("dough")[0]
        if person_patch.overlaps_with(dough_patch.left, dough_patch.lower, dough_patch.right, dough_patch.upper):
            return "yes"
    return image_patch.llm_query("Is this a photo of someone baking dough before it is eaten?")
answer = execute_command(image)