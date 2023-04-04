from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_8_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    tree_patches = image_patch.find("tree")
    car_patches = image_patch.find("car")
    if len(tree_patches) == 0 or len(car_patches) == 0:
        return "no"
    else:
        for tree_patch in tree_patches:
            for car_patch in car_patches:
                if distance(tree_patch, car_patch) < 0:
                    return "yes"
        return "no"
answer = execute_command(image)