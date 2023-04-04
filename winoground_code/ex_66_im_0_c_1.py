from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_66_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.vertical_center)
    shorter_person_patch = person_patches[0]
    taller_person_patch = person_patches[-1]
    if shorter_person_patch.left < taller_person_patch.left and shorter_person_patch.right < taller_person_patch.right:
        return "yes"
    else:
        return "no"
answer = execute_command(image)