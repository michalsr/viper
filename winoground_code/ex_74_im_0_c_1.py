from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_74_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    # Check if there are people walking
    walking_patches = image_patch.find("people walking")
    if not walking_patches:
        return "no"
    # Check if there are people playing instruments
    instrument_patches = image_patch.find("people playing instruments")
    if not instrument_patches:
        return "no"
    # Check if the people playing instruments are standing still or rocking out
    instrument_patches.sort(key=lambda x: x.vertical_center)
    lowest_instrument_patch = instrument_patches[0]
    highest_instrument_patch = instrument_patches[-1]
    if lowest_instrument_patch.vertical_center < walking_patches[0].vertical_center < highest_instrument_patch.vertical_center:
        return "yes"
    else:
        return "no"
answer = execute_command(image)