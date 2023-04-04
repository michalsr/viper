from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_1_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    if len(person_patches) < 2:
        return "no"
    person_patches.sort(key=lambda x: x.height)
    shorter_person_patch = person_patches[0]
    taller_person_patch = person_patches[1]
    if shorter_person_patch.upper > taller_person_patch.lower:
        return "yes"
    else:
        return "no"
answer = execute_command(image)