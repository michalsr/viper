from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_48_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    passenger_patches = image_patch.find("passenger")
    driver_patches = image_patch.find("driver")
    if len(passenger_patches) == 0 or len(driver_patches) == 0:
        return "Unable to determine"
    passenger_patch = passenger_patches[0]
    driver_patch = driver_patches[0]
    if passenger_patch.vertical_center < driver_patch.vertical_center:
        return "no"
    else:
        return "yes"
answer = execute_command(image)