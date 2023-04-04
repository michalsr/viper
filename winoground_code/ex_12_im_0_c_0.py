from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_12_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    computer_patches = image_patch.find("computer")
    book_patches = image_patch.find("book")
    if len(computer_patches) == 0 or len(book_patches) == 0:
        return "no"
    computer_patch = computer_patches[0]
    book_patch = book_patches[0]
    if computer_patch.vertical_center > book_patch.vertical_center:
        return "no"
    return "yes"
answer = execute_command(image)