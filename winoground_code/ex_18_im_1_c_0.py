from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_18_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    orange_juice_patches = image_patch.find("orange juice")
    milk_patches = image_patch.find("milk")
    if len(orange_juice_patches) == 0 or len(milk_patches) == 0:
        return "Cannot determine if there is less orange juice than milk."
    orange_juice_area = orange_juice_patches[0].width * orange_juice_patches[0].height
    milk_area = milk_patches[0].width * milk_patches[0].height
    if orange_juice_area < milk_area:
        return "Yes, there is less orange juice than milk."
    elif orange_juice_area > milk_area:
        return "No, there is more orange juice than milk."
    else:
        return "There is an equal amount of orange juice and milk."
answer = execute_command(image)