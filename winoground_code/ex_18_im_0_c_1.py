from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_18_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    milk_patches = image_patch.find("milk")
    orange_juice_patches = image_patch.find("orange juice")
    if len(milk_patches) == 0 or len(orange_juice_patches) == 0:
        return "Cannot determine if there is less milk than orange juice in the photo."
    milk_patch = milk_patches[0]
    orange_juice_patch = orange_juice_patches[0]
    milk_area = milk_patch.width * milk_patch.height
    orange_juice_area = orange_juice_patch.width * orange_juice_patch.height
    if milk_area < orange_juice_area:
        return "Yes, there is less milk than orange juice in the photo."
    elif milk_area > orange_juice_area:
        return "No, there is more milk than orange juice in the photo."
    else:
        return "There is an equal amount of milk and orange juice in the photo."
answer = execute_command(image)