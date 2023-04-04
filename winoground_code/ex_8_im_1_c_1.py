from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_8_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    car_patches = image_patch.find("car")
    tree_patches = image_patch.find("tree")
    if len(car_patches) == 0 or len(tree_patches) == 0:
        return "no"
    else:
        car_patch = car_patches[0]
        tree_patch = tree_patches[0]
        if car_patch.overlaps_with(tree_patch.left, tree_patch.lower, tree_patch.right, tree_patch.upper):
            return "yes"
        else:
            return "no"
answer = execute_command(image)