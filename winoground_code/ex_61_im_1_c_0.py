from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_61_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    num_people = len(image_patch.find("person"))
    num_windows = len(image_patch.find("window"))
    return bool_to_yesno(num_people == 3 and num_windows == 2)
answer = execute_command(image)