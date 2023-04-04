from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_82_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.horizontal_center)
    patterned_shirt_patch = None
    curly_hair_patch = None
    straight_hair_patch = None
    for person_patch in person_patches:
        if person_patch.verify_property("person", "patterned shirt"):
            patterned_shirt_patch = person_patch
        if person_patch.verify_property("person", "curly hair"):
            curly_hair_patch = person_patch
        if person_patch.verify_property("person", "straight hair"):
            straight_hair_patch = person_patch
    if patterned_shirt_patch is None or curly_hair_patch is None or straight_hair_patch is None:
        return "I'm sorry, I couldn't find all the necessary information in the image."
    if patterned_shirt_patch.horizontal_center < curly_hair_patch.horizontal_center < straight_hair_patch.horizontal_center:
        return "no"
    elif patterned_shirt_patch.horizontal_center > curly_hair_patch.horizontal_center > straight_hair_patch.horizontal_center:
        return "no"
    else:
        return "yes"
answer = execute_command(image)