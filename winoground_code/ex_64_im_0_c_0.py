from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_64_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    dog_leg_patches = image_patch.find("dog's leg")
    person_torso_patches = image_patch.find("person's torso")
    for dog_leg in dog_leg_patches:
        for person_torso in person_torso_patches:
            if dog_leg.overlaps_with(person_torso.left, person_torso.lower, person_torso.right, person_torso.upper):
                return "yes"
    return "no"
answer = execute_command(image)