from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_39_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    hurt_person_patches = image_patch.find("hurt person")
    helpful_person_patches = image_patch.find("helpful person")
    hurt_person_patches.sort(key=lambda x: x.horizontal_center)
    helpful_person_patches.sort(key=lambda x: x.horizontal_center)
    if hurt_person_patches[0].left < helpful_person_patches[0].left:
        return "yes"
    else:
        return "no"
answer = execute_command(image)