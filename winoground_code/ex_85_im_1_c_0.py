from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_85_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    crown_patches = image_patch.find("crown")
    frog_patches = image_patch.find("frog")
    for person in person_patches:
        for crown in crown_patches:
            if person.overlaps_with(crown.left, crown.lower, crown.right, crown.upper):
                for frog in frog_patches:
                    if person.overlaps_with(frog.left, frog.lower, frog.right, frog.upper):
                        return "yes"
    return "no"
answer = execute_command(image)