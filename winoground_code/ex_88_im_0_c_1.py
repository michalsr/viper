from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_88_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    potato_patches = image_patch.find("potatoes")
    meat_patches = image_patch.find("meat")
    if len(potato_patches) > 0 and len(meat_patches) > 0:
        for potato_patch in potato_patches:
            for meat_patch in meat_patches:
                if potato_patch.overlaps_with(meat_patch.left, meat_patch.lower, meat_patch.right, meat_patch.upper):
                    return "yes"
        return "no"
    else:
        return image_patch.llm_query("Is this a photo of potatoes with meat?")
answer = execute_command(image)