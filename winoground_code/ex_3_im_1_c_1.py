from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_3_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    animal_patches = image_patch.find("animal")
    person_patches = image_patch.find("person")
    for animal in animal_patches:
        for person in person_patches:
            if animal.overlaps_with(person.left, person.lower, person.right, person.upper):
                return "yes"
    return "no"
answer = execute_command(image)