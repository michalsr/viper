from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_14_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    grass_patches = image_patch.find("grass")
    mug_patches = image_patch.find("mug")
    for grass in grass_patches:
        for mug in mug_patches:
            if grass.overlaps_with(mug.left, mug.lower, mug.right, mug.upper):
                return "yes"
    return "no"
answer = execute_command(image)