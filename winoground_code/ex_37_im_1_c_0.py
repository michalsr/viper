from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_37_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    shoe_patches = image_patch.find("soft shoes")
    floor_patches = image_patch.find("smooth floor")
    if len(shoe_patches) == 0 or len(floor_patches) == 0:
        return "no"
    shoe_patch = shoe_patches[0]
    floor_patch = floor_patches[0]
    if shoe_patch.overlaps_with(floor_patch.left, floor_patch.lower, floor_patch.right, floor_patch.upper):
        return "yes"
    else:
        return "no"
answer = execute_command(image)