from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_40_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.vertical_center)
    top_person_patch = person_patches[0]
    bottom_person_patch = person_patches[-1]
    top_food_patches = top_person_patch.find("food")
    bottom_food_patches = bottom_person_patch.find("food")
    top_food_patches.sort(key=lambda x: x.horizontal_center)
    bottom_food_patches.sort(key=lambda x: x.horizontal_center)
    top_food_patch = top_food_patches[-1]
    bottom_food_patch = bottom_food_patches[0]
    top_food_healthiness = top_food_patch.simple_query("Is this food healthy?")
    bottom_food_healthiness = bottom_food_patch.simple_query("Is this food healthy?")
    if top_food_healthiness == "yes" and bottom_food_healthiness == "no":
        return "yes"
    else:
        return "no"
answer = execute_command(image)