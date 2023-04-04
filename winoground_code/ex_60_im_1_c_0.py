from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_60_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    toast_patches = image_patch.find("toast")
    egg_patches = image_patch.find("egg")
    toast_patches.sort(key=lambda x: x.horizontal_center)
    egg_patches.sort(key=lambda x: x.horizontal_center)
    if len(toast_patches) >= 1 and len(egg_patches) >= 2:
        toast_patch = toast_patches[0]
        egg_patch_1, egg_patch_2 = egg_patches[:2]
        if toast_patch.overlaps_with(egg_patch_1.left, egg_patch_1.lower, egg_patch_2.right, egg_patch_2.upper):
            return "yes"
    return "no"
answer = execute_command(image)