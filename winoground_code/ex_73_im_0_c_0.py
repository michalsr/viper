from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_73_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    present_patches = image_patch.find("present")
    watch_patches = image_patch.find("watch")
    if len(present_patches) == 0 or len(watch_patches) == 0:
        return "no"
    present_patch = present_patches[0]
    watch_patch = watch_patches[0]
    if present_patch.overlaps_with(watch_patch.left, watch_patch.lower, watch_patch.right, watch_patch.upper):
        return "yes"
    else:
        return "no"
answer = execute_command(image)