from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_21_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    dog_patches = image_patch.find("dog")
    if len(person_patches) == 1 and len(dog_patches) == 1:
        person_patch = person_patches[0]
        dog_patch = dog_patches[0]
        if person_patch.vertical_center > dog_patch.vertical_center:
            return "yes"
    return "no"
answer = execute_command(image)