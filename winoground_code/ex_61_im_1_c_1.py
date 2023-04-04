from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_61_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    num_people = len(image_patch.find("person"))
    num_windows = len(image_patch.find("window"))
    if num_people == 2 and num_windows == 3:
        return "yes"
    else:
        return "no"
answer = execute_command(image)