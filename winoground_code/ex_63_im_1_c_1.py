from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_63_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    people_patches = image_patch.find("person")
    blue_shirts = 0
    white_shirts = 0
    for person in people_patches:
        shirt_color = person.best_text_match(["blue", "white"])
        if shirt_color == "blue":
            blue_shirts += 1
        elif shirt_color == "white":
            white_shirts += 1
    if blue_shirts == 6 and white_shirts == 0:
        return "yes"
    else:
        return "no"
answer = execute_command(image)