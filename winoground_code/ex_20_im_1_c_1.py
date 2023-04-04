from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_20_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    white_chocolate_patches = image_patch.find("white chocolate")
    milk_chocolate_patches = image_patch.find("milk chocolate")
    if len(white_chocolate_patches) == 0 or len(milk_chocolate_patches) == 0:
        return "Cannot determine chocolate ratio"
    white_chocolate_area = sum([patch.width * patch.height for patch in white_chocolate_patches])
    milk_chocolate_area = sum([patch.width * patch.height for patch in milk_chocolate_patches])
    if white_chocolate_area < milk_chocolate_area:
        return "Yes"
    else:
        return "No"
answer = execute_command(image)