from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_10_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    sail_rests_patches = image_patch.find("sail rests")
    water_patches = image_patch.find("water")
    for sail_rests_patch in sail_rests_patches:
        for water_patch in water_patches:
            if sail_rests_patch.overlaps_with(water_patch.left, water_patch.lower, water_patch.right, water_patch.upper):
                return "yes"
    return "no"
answer = execute_command(image)