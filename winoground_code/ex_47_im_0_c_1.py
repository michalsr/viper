from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_47_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    sailboat_patches = image_patch.find("sailboat")
    if not sailboat_patches:
        return "No sailboat found in the image."
    sailboat_patch = sailboat_patches[0]
    beach_patches = image_patch.find("beach")
    if not beach_patches:
        return "No beach found in the image."
    beach_patch = beach_patches[0]
    if sailboat_patch.compute_depth() > beach_patch.compute_depth():
        return "Yes, the sailboat sails are far away and the beach is close."
    else:
        return "No, the sailboat sails are not far away or the beach is not close."
answer = execute_command(image)