from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_69_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    people_in_boat = image_patch.find("person in boat")
    swimming_person = image_patch.find("swimming person")
    if len(people_in_boat) + len(swimming_person) == len(image_patch.find("person")):
        return "yes"
    else:
        return "no"
answer = execute_command(image)