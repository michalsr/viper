from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_83_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    # Check if there are arrows in the image
    if not image_patch.exists("arrow"):
        return "No arrows found in the image."
    # Sort the arrows by horizontal position
    arrow_patches = image_patch.find("arrow")
    arrow_patches.sort(key=lambda x: x.horizontal_center)
    # Check if the arrows are moving from left to right
    for i in range(len(arrow_patches)-1):
        if arrow_patches[i].horizontal_center > arrow_patches[i+1].horizontal_center:
            return "Arrows are not moving from left to right."
    return "This is a photo of a diagram showing movement from left to right."
answer = execute_command(image)