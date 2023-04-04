from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_83_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    # Check if there are arrows in the image
    if not image_patch.exists("arrow"):
        return "No arrows found in the image."
    # Find the leftmost and rightmost arrows
    arrow_patches = image_patch.find("arrow")
    arrow_patches.sort(key=lambda x: x.horizontal_center)
    left_arrow = arrow_patches[0]
    right_arrow = arrow_patches[-1]
    # Check if the left arrow is to the right of the right arrow
    if left_arrow.horizontal_center > right_arrow.horizontal_center:
        return "Yes, this is a photo of a diagram showing movement from right to left."
    else:
        return "No, this is not a photo of a diagram showing movement from right to left."
answer = execute_command(image)