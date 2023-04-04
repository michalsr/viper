from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_30_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    bird_patches = image_patch.find("bird")
    berry_patches = image_patch.find("berry")
    if len(bird_patches) == 0 or len(berry_patches) == 0:
        return "no"
    bird_patch = bird_patches[0]
    berry_patch = berry_patches[0]
    if bird_patch.best_text_match(["red"]) == "red" and berry_patch.best_text_match(["blue"]) == "blue":
        if bird_patch.overlaps_with(berry_patch.left - 10, berry_patch.lower - 10, berry_patch.right + 10, berry_patch.upper + 10):
            return "yes"
    return "no"
answer = execute_command(image)