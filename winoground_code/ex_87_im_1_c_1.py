from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_87_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    bird_patches = image_patch.find("caged bird")
    for bird_patch in bird_patches:
        if bird_patch.verify_property("caged bird", "unopened cage door"):
            return "yes"
    return "no"
answer = execute_command(image)