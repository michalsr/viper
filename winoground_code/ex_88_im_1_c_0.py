from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_88_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    meat_patches = image_patch.find("meat")
    potato_patches = image_patch.find("potatoes")
    if len(meat_patches) > 0 and len(potato_patches) > 0:
        for meat_patch in meat_patches:
            for potato_patch in potato_patches:
                if distance(meat_patch, potato_patch) < 0:
                    return "yes"
    return image_patch.llm_query("What is in this photo?")
answer = execute_command(image)