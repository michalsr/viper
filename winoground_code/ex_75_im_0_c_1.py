from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_75_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    kid_patches = image_patch.find("kid")
    magnifying_glass_patches = image_patch.find("magnifying glass")
    for kid_patch in kid_patches:
        for magnifying_glass_patch in magnifying_glass_patches:
            if kid_patch.overlaps_with(magnifying_glass_patch.left, magnifying_glass_patch.lower, magnifying_glass_patch.right, magnifying_glass_patch.upper):
                return "yes"
    return "no"
answer = execute_command(image)