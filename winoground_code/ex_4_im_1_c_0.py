from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_4_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_without_earrings_patches = image_patch.find("person without earrings")
    person_with_earrings_patches = image_patch.find("person with earrings")
    if len(person_without_earrings_patches) == 0 or len(person_with_earrings_patches) == 0:
        return "Cannot determine"
    person_without_earrings_patch = person_without_earrings_patches[0]
    person_with_earrings_patch = person_with_earrings_patches[0]
    if person_without_earrings_patch.horizontal_center < person_with_earrings_patch.horizontal_center:
        return "yes"
    else:
        return "no"
answer = execute_command(image)