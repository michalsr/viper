from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_66_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.vertical_center)
    taller_person_patch = person_patches[-1]
    shorter_person_patch = person_patches[0]
    if taller_person_patch.left < shorter_person_patch.left:
        arm_patch = image_patch.crop(taller_person_patch.right, taller_person_patch.vertical_center, shorter_person_patch.left, shorter_person_patch.vertical_center)
    else:
        arm_patch = image_patch.crop(shorter_person_patch.right, shorter_person_patch.vertical_center, taller_person_patch.left, taller_person_patch.vertical_center)
    if arm_patch.verify_property("arm", "around") and arm_patch.verify_property("arm", "shoulder"):
        return "yes"
    else:
        return "no"
answer = execute_command(image)