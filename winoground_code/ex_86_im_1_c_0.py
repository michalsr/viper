from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_86_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    dog_patches = image_patch.find("dog")
    couch_patches = image_patch.find("couch")
    person_patches = image_patch.find("person")
    lying_patches = image_patch.find("lying")
    if len(dog_patches) == 0 or len(couch_patches) == 0 or len(person_patches) == 0 or len(lying_patches) == 0:
        return "no"
    dog_patch = dog_patches[0]
    couch_patch = couch_patches[0]
    person_patch = person_patches[0]
    lying_patch = lying_patches[0]
    if dog_patch.vertical_center < couch_patch.vertical_center or dog_patch.horizontal_center < couch_patch.left or dog_patch.horizontal_center > couch_patch.right:
        return "no"
    if person_patch.vertical_center > lying_patch.vertical_center or person_patch.horizontal_center < couch_patch.left or person_patch.horizontal_center > couch_patch.right:
        return "no"
    return "yes"
answer = execute_command(image)