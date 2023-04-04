from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_62_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    left_flag_patches = image_patch.find("left flag")
    right_flag_patches = image_patch.find("right flag")
    left_flag_patch = left_flag_patches[0]
    right_flag_patch = right_flag_patches[0]
    left_flag_stars = left_flag_patch.simple_query("How many stars are on the left flag?")
    right_flag_stars = right_flag_patch.simple_query("How many stars are on the right flag?")
    if coerce_to_numeric(left_flag_stars) == 50 and coerce_to_numeric(right_flag_stars) == 5:
        return "yes"
    else:
        return "no"
answer = execute_command(image)