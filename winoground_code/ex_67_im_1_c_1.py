from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_67_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    black_coat_patches = image_patch.find("person in black coat")
    brown_coat_patches = image_patch.find("person in brown coat")
    if len(black_coat_patches) == 1 and len(brown_coat_patches) == 1:
        black_coat_patch = black_coat_patches[0]
        brown_coat_patch = brown_coat_patches[0]
        if black_coat_patch.horizontal_center < brown_coat_patch.horizontal_center:
            return "no"
        else:
            return "yes"
    else:
        return image_patch.llm_query("Is this a photo of the person in a black coat looks back and the person in a brown coat looks forward?")
answer = execute_command(image)