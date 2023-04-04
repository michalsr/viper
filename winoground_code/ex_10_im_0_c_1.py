from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_10_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    water_patches = image_patch.find("water")
    sail_patches = image_patch.find("sail")
    if len(water_patches) == 0 or len(sail_patches) == 0:
        return "Cannot determine if the water rests below the sail."
    water_patch = water_patches[0]
    sail_patch = sail_patches[0]
    if water_patch.vertical_center < sail_patch.vertical_center:
        return "Yes, the water rests below the sail."
    else:
        return "No, the water does not rest below the sail."
answer = execute_command(image)