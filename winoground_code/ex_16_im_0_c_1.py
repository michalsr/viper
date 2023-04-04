from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_16_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    spoon_patches = image_patch.find("spoon")
    fork_patches = image_patch.find("fork")
    if len(spoon_patches) < len(fork_patches):
        return "yes"
    else:
        return "no"
answer = execute_command(image)