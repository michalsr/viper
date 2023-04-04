from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_95_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    hammer_patches = image_patch.find("hammer")
    if len(hammer_patches) == 0:
        return "no"
    hammer_patches.sort(key=lambda x: x.vertical_center)
    top_hammer_patch = hammer_patches[0]
    if top_hammer_patch.vertical_center < image_patch.vertical_center:
        return "yes"
    else:
        return "no"
answer = execute_command(image)