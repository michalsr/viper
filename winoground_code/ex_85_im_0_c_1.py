from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_85_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    frog_patches = image_patch.find("frog")
    crown_patches = image_patch.find("crown")
    if len(person_patches) == 0 or len(frog_patches) == 0 or len(crown_patches) == 0:
        return "no"
    person_patch = person_patches[0]
    frog_patch = frog_patches[0]
    crown_patch = crown_patches[0]
    if person_patch.overlaps_with(frog_patch.left, frog_patch.lower, frog_patch.right, frog_patch.upper) and \
            frog_patch.overlaps_with(crown_patch.left, crown_patch.lower, crown_patch.right, crown_patch.upper):
        return "yes"
    else:
        return "no"
answer = execute_command(image)