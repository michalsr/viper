from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_60_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    toast_patches = image_patch.find("toast")
    egg_patches = image_patch.find("egg")
    toast_patches.sort(key=lambda x: x.horizontal_center)
    egg_patches.sort(key=lambda x: x.horizontal_center)
    if len(toast_patches) >= 2 and len(egg_patches) >= 1:
        if toast_patches[0].overlaps_with(toast_patches[1].left, toast_patches[1].lower, toast_patches[1].right, toast_patches[1].upper) and egg_patches[0].overlaps_with(toast_patches[0].left, toast_patches[0].lower, toast_patches[1].right, toast_patches[1].upper):
            return "yes"
    return "no"
answer = execute_command(image)