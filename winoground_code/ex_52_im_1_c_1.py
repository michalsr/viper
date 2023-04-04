from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_52_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    frog_patches = image_patch.find("frog")
    rock_patches = image_patch.find("rock")
    water_patches = image_patch.find("water")
    if len(frog_patches) == 0 or len(rock_patches) == 0 or len(water_patches) == 0:
        return "no"
    frog_patch = frog_patches[0]
    rock_patch = rock_patches[0]
    water_patch = water_patches[0]
    if frog_patch.vertical_center > rock_patch.vertical_center or rock_patch.vertical_center > water_patch.vertical_center:
        return "no"
    return "yes"
answer = execute_command(image)