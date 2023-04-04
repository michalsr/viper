from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_19_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    jar_patches = image_patch.find("jar")
    jar_patch = jar_patches[0]
    dirt_patches = jar_patch.find("dirt")
    empty_space_patches = jar_patch.find("empty space")
    if len(dirt_patches) == 0 or len(empty_space_patches) == 0:
        return "Cannot determine if there is more empty space than dirt in the jar."
    dirt_area = sum([patch.width * patch.height for patch in dirt_patches])
    empty_space_area = sum([patch.width * patch.height for patch in empty_space_patches])
    if empty_space_area > dirt_area:
        return "Yes, there is more empty space than dirt in the jar."
    else:
        return "No, there is not more empty space than dirt in the jar."
answer = execute_command(image)