from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_0_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    people_patches = image_patch.find("person")
    if len(people_patches) < 2:
        return "no"
    people_patches.sort(key=lambda x: x.vertical_center)
    young_person_patch, old_person_patch = people_patches[0], people_patches[-1]
    if young_person_patch.horizontal_center < old_person_patch.horizontal_center:
        return "yes"
    else:
        return "no"
answer = execute_command(image)