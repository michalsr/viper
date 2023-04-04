from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_64_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    dog_patches = image_patch.find("dog")
    for person in person_patches:
        for dog in dog_patches:
            if person.overlaps_with(dog.left, dog.lower, dog.right, dog.upper):
                return "yes"
    return "no"
answer = execute_command(image)