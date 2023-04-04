from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_50_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    green_legs_patches = image_patch.find("person with green legs")
    red_legs_patches = image_patch.find("person with red legs")
    if len(green_legs_patches) == 0 or len(red_legs_patches) == 0:
        return "No"
    green_legs_patch = green_legs_patches[0]
    red_legs_patch = red_legs_patches[0]
    if green_legs_patch.verify_property("person with green legs", "running quite slowly") and red_legs_patch.verify_property("person with red legs", "running faster"):
        return "Yes"
    else:
        return "No"
answer = execute_command(image)