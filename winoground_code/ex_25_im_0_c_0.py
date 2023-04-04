from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_25_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches = [p for p in person_patches if p.verify_property("person", "white collared shirt")]
    if len(person_patches) != 2:
        return "no"
    person_patches.sort(key=lambda x: x.horizontal_center)
    left_person, right_person = person_patches
    plant_patches = image_patch.find("plant")
    if not plant_patches:
        return "no"
    plant_patch = plant_patches[0]
    if plant_patch.overlaps_with(left_person.left, left_person.lower, right_person.right, right_person.upper):
        return "yes"
    else:
        return "no"
answer = execute_command(image)