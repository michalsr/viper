from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_55_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    green_patches = image_patch.find("green")
    blue_patches = image_patch.find("blue")
    if len(green_patches) == 0 or len(blue_patches) == 0:
        return "No green or blue objects found in the image."
    green_patch = green_patches[0]
    blue_patch = blue_patches[0]
    if green_patch.width < blue_patch.width or green_patch.height < blue_patch.height:
        return "The blue object cannot fit inside the green object."
    if green_patch.width > blue_patch.width and green_patch.height > blue_patch.height:
        return "The green object cannot fit inside the blue object."
    if green_patch.width > blue_patch.width and green_patch.height < blue_patch.height:
        return "The blue object can fit inside the green object, but the green object cannot fit inside the blue object."
    if green_patch.width < blue_patch.width and green_patch.height > blue_patch.height:
        return "The green object can fit inside the blue object, but the blue object cannot fit inside the green object."
    if green_patch.width == blue_patch.width and green_patch.height == blue_patch.height:
        return "The green and blue objects are the same size and cannot fit inside each other."
    return "Unknown error occurred."
answer = execute_command(image)