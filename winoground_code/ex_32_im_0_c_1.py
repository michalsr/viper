from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_32_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    astronaut_patches = image_patch.find("astronauts")
    if len(astronaut_patches) == 0:
        return "no"
    astronaut_patch = astronaut_patches[0]
    if not astronaut_patch.verify_property("astronauts", "red suits"):
        return "no"
    planet_patches = image_patch.find("planet")
    if len(planet_patches) == 0:
        return "no"
    planet_patch = planet_patches[0]
    if not planet_patch.verify_property("planet", "blue"):
        return "no"
    return "yes"
answer = execute_command(image)