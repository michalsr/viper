from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_87_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    bird_patches = image_patch.find("uncaged bird")
    if len(bird_patches) == 0:
        return "no"
    bird_patch = bird_patches[0]
    cage_patches = image_patch.find("cage")
    if len(cage_patches) == 0:
        return "no"
    cage_patch = cage_patches[0]
    if bird_patch.overlaps_with(cage_patch.left, cage_patch.lower, cage_patch.right, cage_patch.upper):
        return "yes"
    else:
        return "no"
answer = execute_command(image)