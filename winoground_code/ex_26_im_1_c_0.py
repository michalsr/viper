from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_26_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.height, reverse=True)
    taller_person_patch = person_patches[0]
    shorter_person_patch = person_patches[1]
    food_patches = image_patch.find("food")
    food_patches.sort(key=lambda x: x.vertical_center)
    food_patch = food_patches[0]
    if taller_person_patch.overlaps_with(food_patch.left, food_patch.lower, food_patch.right, food_patch.upper) and \
            shorter_person_patch.overlaps_with(food_patch.left, food_patch.lower, food_patch.right, food_patch.upper):
        return "yes"
    else:
        return "no"
answer = execute_command(image)