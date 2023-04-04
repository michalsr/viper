from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_80_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    watering_can_patches = image_patch.find("watering can")
    pot_patches = image_patch.find("pot")
    if len(watering_can_patches) == 0 or len(pot_patches) == 0:
        return "Cannot determine"
    watering_can_patch = watering_can_patches[0]
    pot_patch = pot_patches[0]
    if watering_can_patch.width * watering_can_patch.height > pot_patch.width * pot_patch.height:
        return "yes"
    else:
        return "no"
answer = execute_command(image)