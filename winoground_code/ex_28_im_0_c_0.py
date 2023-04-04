from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_28_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    if len(person_patches) == 0:
        return "no"
    person_patch = person_patches[0]
    flower_patches = image_patch.find("flower")
    yellow_flower_patches = [patch for patch in flower_patches if patch.best_text_match(["yellow"])]
    if len(yellow_flower_patches) == 0:
        return "no"
    yellow_flower_patch = yellow_flower_patches[0]
    if not person_patch.overlaps_with(yellow_flower_patch.left, yellow_flower_patch.lower, yellow_flower_patch.right, yellow_flower_patch.upper):
        return "no"
    dress_patches = image_patch.find("dress")
    red_dress_patches = [patch for patch in dress_patches if patch.best_text_match(["red"])]
    if len(red_dress_patches) == 0:
        return "no"
    red_dress_patch = red_dress_patches[0]
    if not person_patch.overlaps_with(red_dress_patch.left, red_dress_patch.lower, red_dress_patch.right, red_dress_patch.upper):
        return "no"
    return "yes"
answer = execute_command(image)