from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_22_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.horizontal_center)
    person_with_more_hair = person_patches[-1]
    person_with_less_hair = person_patches[0]
    if person_with_more_hair.verify_property("person", "facial hair") and not person_with_less_hair.verify_property("person", "facial hair"):
        return "yes"
    else:
        return "no"
answer = execute_command(image)