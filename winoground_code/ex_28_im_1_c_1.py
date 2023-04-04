from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_28_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    if len(person_patches) == 0:
        return "no"
    person_patch = person_patches[0]
    if not person_patch.verify_property("person", "walking"):
        return "no"
    flower_patches = image_patch.find("flower")
    red_flower_patches = [patch for patch in flower_patches if patch.best_text_match(["red", "pink"]) == "red"]
    if len(red_flower_patches) == 0:
        return "no"
    yellow_dress_patches = person_patch.find("yellow dress")
    if len(yellow_dress_patches) == 0:
        return "no"
    yellow_dress_patch = yellow_dress_patches[0]
    if not yellow_dress_patch.overlaps_with(*person_patch):
        return "no"
    return "yes"
answer = execute_command(image)