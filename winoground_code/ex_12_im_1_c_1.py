from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_12_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    books_patches = image_patch.find("books")
    computer_patches = image_patch.find("computer")
    if len(books_patches) == 0 or len(computer_patches) == 0:
        return "no"
    books_patch = books_patches[0]
    computer_patch = computer_patches[0]
    if books_patch.vertical_center > computer_patch.vertical_center:
        return "yes"
    else:
        return "no"
answer = execute_command(image)