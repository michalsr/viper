from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_43_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    cat_patches = image_patch.find("big cat")
    dog_patches = image_patch.find("small dog")
    if len(cat_patches) == 0 or len(dog_patches) == 0:
        return "no"
    cat_patch = cat_patches[0]
    dog_patch = dog_patches[0]
    if cat_patch.horizontal_center < dog_patch.horizontal_center:
        return "yes"
    else:
        return "no"
answer = execute_command(image)