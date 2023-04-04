from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_37_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    shoe_patches = image_patch.find("shoes")
    floor_patches = image_patch.find("floor")
    if len(shoe_patches) == 0 or len(floor_patches) == 0:
        return "no"
    shoe_patches.sort(key=lambda x: x.compute_depth())
    floor_patches.sort(key=lambda x: x.compute_depth())
    shoe_patch = shoe_patches[0]
    floor_patch = floor_patches[0]
    if shoe_patch.verify_property("shoes", "smooth") and floor_patch.verify_property("floor", "soft"):
        return "yes"
    else:
        return "no"
answer = execute_command(image)