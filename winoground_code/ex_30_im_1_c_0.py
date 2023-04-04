from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_30_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    bird_patches = image_patch.find("bird")
    berry_patches = image_patch.find("berry")
    if len(bird_patches) == 0 or len(berry_patches) == 0:
        return "no"
    bird_patch = bird_patches[0]
    berry_patch = berry_patches[0]
    if bird_patch.horizontal_center < berry_patch.horizontal_center:
        left_patch = bird_patch
        right_patch = berry_patch
    else:
        left_patch = berry_patch
        right_patch = bird_patch
    if left_patch.verify_property("bird", "blue") and right_patch.verify_property("berry", "red"):
        return "yes"
    else:
        return "no"
answer = execute_command(image)