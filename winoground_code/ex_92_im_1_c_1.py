from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_92_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    if len(person_patches) < 2:
        return "no"
    person_patches.sort(key=lambda x: x.horizontal_center)
    person1_patch = person_patches[0]
    person2_patch = person_patches[1]
    if person1_patch.verify_property("person", "talking on phone") and person1_patch.verify_property("person", "happy") and person2_patch.verify_property("person", "sitting") and person2_patch.verify_property("person", "angry"):
        return "yes"
    else:
        return "no"
answer = execute_command(image)