from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_77_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    people_patches = image_patch.find("people")
    if len(people_patches) < 2:
        return "no"
    people_patches.sort(key=lambda x: x.vertical_center)
    if people_patches[0].overlaps_with(people_patches[1].left, people_patches[1].lower, people_patches[1].right, people_patches[1].upper):
        return "yes"
    return "no"
answer = execute_command(image)