from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_92_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    if len(person_patches) < 2:
        return "no"
    person_patches.sort(key=lambda x: x.horizontal_center)
    person1_patch = person_patches[0]
    person2_patch = person_patches[1]
    if person1_patch.verify_property("person", "angry") and person2_patch.verify_property("person", "happy"):
        phone_patches = image_patch.find("phone")
        if len(phone_patches) > 0:
            phone_patch = phone_patches[0]
            if phone_patch.overlaps_with(person1_patch.left, person1_patch.lower, person1_patch.right, person1_patch.upper):
                return "yes"
    return "no"
answer = execute_command(image)