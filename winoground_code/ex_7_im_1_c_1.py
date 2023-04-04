from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_7_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    water_patches = image_patch.find("water")
    bottle_patches = image_patch.find("bottle")
    for water_patch in water_patches:
        for bottle_patch in bottle_patches:
            if distance(water_patch, bottle_patch) < 0:
                return "yes"
    return "no"
answer = execute_command(image)