from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_91_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    clothes_patches = image_patch.find("clothing")
    if len(clothes_patches) == 0:
        return "no"
    clothes_patches.sort(key=lambda x: x.vertical_center)
    top_clothes_patch = clothes_patches[0]
    bottom_clothes_patch = clothes_patches[-1]
    if top_clothes_patch.overlaps_with(0, bottom_clothes_patch.upper, image_patch.width, top_clothes_patch.lower):
        return "yes"
    else:
        return "no"
answer = execute_command(image)