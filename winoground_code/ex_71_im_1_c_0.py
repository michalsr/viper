from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_71_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    neutral_patches = image_patch.find("person wearing neutral colors")
    bright_patches = image_patch.find("person wearing brighter colors")
    if len(neutral_patches) == 1 and len(bright_patches) == 1:
        neutral_patch = neutral_patches[0]
        bright_patch = bright_patches[0]
        if neutral_patch.vertical_center > bright_patch.vertical_center:
            return bool_to_yesno(neutral_patch.horizontal_center < bright_patch.horizontal_center)
    return image_patch.llm_query("Is this a photo of the person wearing neutral colors poses and the person wearing brighter colors takes a picture?")
answer = execute_command(image)