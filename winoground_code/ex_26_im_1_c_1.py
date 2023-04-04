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
    for food_patch in food_patches:
        if taller_person_patch.overlaps_with(food_patch.left, food_patch.lower, food_patch.right, food_patch.upper):
            taller_person_eats = True
        if shorter_person_patch.overlaps_with(food_patch.left, food_patch.lower, food_patch.right, food_patch.upper):
            shorter_person_chops = True
    if taller_person_eats and shorter_person_chops:
        return "Yes, this is a photo of the taller person eating food and the shorter person chopping food."
    else:
        return "No, this is not a photo of the taller person eating food and the shorter person chopping food."
answer = execute_command(image)