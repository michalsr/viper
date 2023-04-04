from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_79_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    table_patches = image_patch.find("table")
    food_patches = image_patch.find("food")
    if len(person_patches) == 0 or len(table_patches) == 0 or len(food_patches) == 0:
        return "Cannot answer the question"
    person_patch = person_patches[0]
    table_patch = table_patches[0]
    food_patch = food_patches[0]
    if person_patch.overlaps_with(table_patch.left, table_patch.lower, table_patch.right, table_patch.upper) and \
            food_patch.overlaps_with(table_patch.left, table_patch.lower, table_patch.right, table_patch.upper):
        return "yes"
    else:
        return "no"
answer = execute_command(image)