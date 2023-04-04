from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_20_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    milk_chocolate_patches = image_patch.find("milk chocolate")
    white_chocolate_patches = image_patch.find("white chocolate")
    if len(milk_chocolate_patches) == 0 or len(white_chocolate_patches) == 0:
        return "Cannot determine chocolate ratio"
    milk_chocolate_area = milk_chocolate_patches[0].width * milk_chocolate_patches[0].height
    white_chocolate_area = white_chocolate_patches[0].width * white_chocolate_patches[0].height
    if milk_chocolate_area < white_chocolate_area:
        return "Yes"
    else:
        return "No"
answer = execute_command(image)