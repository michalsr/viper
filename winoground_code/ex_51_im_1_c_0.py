from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_51_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    for person_patch in person_patches:
        if person_patch.verify_property("person", "in water") and person_patch.verify_property("person", "close to sand"):
            return "yes"
    return "no"
answer = execute_command(image)