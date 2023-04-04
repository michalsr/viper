from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_2_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    masked_wrestler_patches = image_patch.find("masked wrestler")
    unmasked_wrestler_patches = image_patch.find("unmasked wrestler")
    for masked_wrestler in masked_wrestler_patches:
        for unmasked_wrestler in unmasked_wrestler_patches:
            if masked_wrestler.horizontal_center < unmasked_wrestler.horizontal_center:
                return "yes"
    return "no"
answer = execute_command(image)