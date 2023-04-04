from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_2_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    unmasked_wrestler_patches = image_patch.find("unmasked wrestler")
    masked_wrestler_patches = image_patch.find("masked wrestler")
    if len(unmasked_wrestler_patches) == 0 or len(masked_wrestler_patches) == 0:
        return "Cannot determine if the unmasked wrestler hits the masked wrestler."
    unmasked_wrestler_patch = unmasked_wrestler_patches[0]
    masked_wrestler_patch = masked_wrestler_patches[0]
    if unmasked_wrestler_patch.overlaps_with(masked_wrestler_patch.left, masked_wrestler_patch.lower, masked_wrestler_patch.right, masked_wrestler_patch.upper):
        return "Yes, this is a photo of the unmasked wrestler hitting the masked wrestler."
    else:
        return "No, this is not a photo of the unmasked wrestler hitting the masked wrestler."
answer = execute_command(image)