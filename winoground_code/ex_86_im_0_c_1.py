from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_86_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    couch_patches = image_patch.find("couch")
    dog_patches = image_patch.find("dog")
    if len(person_patches) == 0 or len(couch_patches) == 0 or len(dog_patches) == 0:
        return "no"
    person_patch = person_patches[0]
    couch_patch = couch_patches[0]
    dog_patch = dog_patches[0]
    if person_patch.vertical_center > couch_patch.vertical_center or not dog_patch.overlaps_with(couch_patch.left, couch_patch.lower, couch_patch.right, couch_patch.upper):
        return "no"
    return "yes"
answer = execute_command(image)