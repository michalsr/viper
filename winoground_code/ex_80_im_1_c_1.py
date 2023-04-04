from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_80_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    pot_patches = image_patch.find("pot")
    watering_can_patches = image_patch.find("watering can")
    if len(pot_patches) == 0 or len(watering_can_patches) == 0:
        return "Unable to find both pot and watering can in the image."
    pot_patch = pot_patches[0]
    watering_can_patch = watering_can_patches[0]
    if pot_patch.width * pot_patch.height > watering_can_patch.width * watering_can_patch.height:
        return "yes"
    else:
        return "no"
answer = execute_command(image)