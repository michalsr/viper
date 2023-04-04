from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_3_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    animal_patches = image_patch.find("animal")
    if len(person_patches) == 1 and len(animal_patches) == 1:
        person_patch = person_patches[0]
        animal_patch = animal_patches[0]
        if person_patch.vertical_center > animal_patch.vertical_center:
            return "yes"
    return "no"
answer = execute_command(image)