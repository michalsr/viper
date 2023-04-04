from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_4_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    earring_patches = image_patch.find("earrings")
    if len(earring_patches) != 2:
        return "Cannot determine if the person with earrings pays the person without earrings."
    earring_patches.sort(key=lambda x: x.horizontal_center)
    left_earring_patch, right_earring_patch = earring_patches
    person_patches = image_patch.find("person")
    if len(person_patches) != 2:
        return "Cannot determine if the person with earrings pays the person without earrings."
    person_patches.sort(key=lambda x: x.horizontal_center)
    left_person_patch, right_person_patch = person_patches
    if left_earring_patch.overlaps_with(left_person_patch.left, left_person_patch.lower, left_person_patch.right, left_person_patch.upper):
        return "The person with earrings pays the person without earrings."
    elif right_earring_patch.overlaps_with(right_person_patch.left, right_person_patch.lower, right_person_patch.right, right_person_patch.upper):
        return "The person without earrings pays the person with earrings."
    else:
        return "Cannot determine if the person with earrings pays the person without earrings."
answer = execute_command(image)