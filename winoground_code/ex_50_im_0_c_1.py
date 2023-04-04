from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_50_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    green_legged_person_patches = image_patch.find("person with green legs")
    red_legged_person_patches = image_patch.find("person with red legs")
    if len(green_legged_person_patches) == 0 or len(red_legged_person_patches) == 0:
        return "No, there are no people with green and red legs in the photo."
    green_legged_person_patch = green_legged_person_patches[0]
    red_legged_person_patch = red_legged_person_patches[0]
    if green_legged_person_patch.horizontal_center > red_legged_person_patch.horizontal_center:
        return "No, the person with green legs is running slower than the person with red legs."
    else:
        return "Yes, the person with green legs is running faster than the person with red legs."
answer = execute_command(image)