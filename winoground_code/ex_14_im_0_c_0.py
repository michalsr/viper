from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_14_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    mug_patches = image_patch.find("mug")
    grass_patches = image_patch.find("grass")
    for mug in mug_patches:
        for grass in grass_patches:
            if mug.overlaps_with(grass.left, grass.lower, grass.right, grass.upper):
                return "yes"
    return "no"
answer = execute_command(image)