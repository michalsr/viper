from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_42_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    if len(person_patches) < 2:
        return "no"
    person_patches.sort(key=lambda x: x.width * x.height)
    smaller_person_patch = person_patches[0]
    larger_person_patch = person_patches[1]
    smaller_person_color = smaller_person_patch.best_text_match(["yellow", "not yellow"])
    larger_person_color = larger_person_patch.best_text_match(["yellow", "not yellow"])
    if smaller_person_color == "yellow" and larger_person_color == "not yellow":
        return "yes"
    else:
        return "no"
answer = execute_command(image)