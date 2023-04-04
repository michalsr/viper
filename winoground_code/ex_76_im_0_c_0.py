from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_76_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.vertical_center)
    person_patch = person_patches[0]
    kid_patches = image_patch.find("kid")
    kid_patches.sort(key=lambda x: x.horizontal_center)
    if person_patch.left < kid_patches[0].left and person_patch.right > kid_patches[-1].right:
        return "yes"
    else:
        return "no"
answer = execute_command(image)