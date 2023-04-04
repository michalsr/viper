from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_70_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.horizontal_center)
    darker_shoes_person = person_patches[0]
    lighter_shoes_person = person_patches[1]
    darker_shoes_person_emoji = darker_shoes_person.find("emoji")
    lighter_shoes_person_emoji = lighter_shoes_person.find("emoji")
    if darker_shoes_person_emoji and not lighter_shoes_person_emoji:
        return "yes"
    else:
        return "no"
answer = execute_command(image)