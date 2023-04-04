from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_19_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    jar_patches = image_patch.find("jar")
    jar_patch = jar_patches[0]
    dirt_patches = jar_patch.find("dirt")
    empty_patches = jar_patch.find("empty space")
    if len(dirt_patches) > len(empty_patches):
        return "yes"
    else:
        return "no"
answer = execute_command(image)