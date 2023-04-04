from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_40_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.vertical_center)
    less_content_person_patch = person_patches[0]
    more_content_person_patch = person_patches[-1]
    less_content_food_patch = less_content_person_patch.crop(less_content_person_patch.left, less_content_person_patch.lower, less_content_person_patch.horizontal_center, less_content_person_patch.upper)
    more_content_food_patch = more_content_person_patch.crop(more_content_person_patch.horizontal_center, more_content_person_patch.lower, more_content_person_patch.right, more_content_person_patch.upper)
    less_content_food_healthiness = less_content_food_patch.simple_query("Is this food healthy?")
    more_content_food_healthiness = more_content_food_patch.simple_query("Is this food healthy?")
    if less_content_food_healthiness == "yes" and more_content_food_healthiness == "no":
        return "yes"
    else:
        return "no"
answer = execute_command(image)