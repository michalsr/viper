from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_65_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    animal_patches = image_patch.find("animal")
    if len(person_patches) == 0 or len(animal_patches) == 0:
        return "Cannot determine"
    person_patch = person_patches[0]
    animal_patch = animal_patches[0]
    if person_patch.width * person_patch.height > animal_patch.width * animal_patch.height:
        return "yes"
    else:
        return "no"
answer = execute_command(image)