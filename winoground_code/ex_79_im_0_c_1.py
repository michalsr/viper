from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_79_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    food_patches = image_patch.find("food")
    table_patches = image_patch.find("table")
    if len(person_patches) == 0 or len(food_patches) == 0 or len(table_patches) == 0:
        return "Cannot determine if this is a photo of the person eating the food on the table."
    person_patch = person_patches[0]
    food_patch = food_patches[0]
    table_patch = table_patches[0]
    if person_patch.vertical_center > food_patch.vertical_center or not table_patch.overlaps_with(food_patch.left, food_patch.lower, food_patch.right, food_patch.upper):
        return "No, this is not a photo of the person eating the food on the table."
    else:
        return "Yes, this is a photo of the person eating the food on the table."
answer = execute_command(image)