from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_63_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    blue_shirts = image_patch.find("blue shirt")
    white_shirts = image_patch.find("white shirt")
    if len(blue_shirts) == 0 or len(white_shirts) != 6:
        return "no"
    blue_shirts.sort(key=lambda x: x.compute_depth())
    white_shirts.sort(key=lambda x: x.compute_depth())
    for i in range(6):
        if blue_shirts[i].overlaps_with(white_shirts[i].left, white_shirts[i].lower, white_shirts[i].right, white_shirts[i].upper):
            return "no"
    return "yes"
answer = execute_command(image)