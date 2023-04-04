from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_42_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    if len(person_patches) < 2:
        return "no"
    person_patches.sort(key=lambda x: x.width * x.height, reverse=True)
    larger_person_patch = person_patches[0]
    smaller_person_patch = person_patches[1]
    if larger_person_patch.verify_property("person", "yellow") and not smaller_person_patch.verify_property("person", "yellow"):
        return "yes"
    else:
        return "no"
answer = execute_command(image)