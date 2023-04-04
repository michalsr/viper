from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_31_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    yellow_book_patches = image_patch.find("yellow book")
    blue_book_patches = image_patch.find("blue book")
    red_book_patches = image_patch.find("red book")
    if len(yellow_book_patches) == 0 or len(blue_book_patches) == 0 or len(red_book_patches) == 0:
        return "Cannot determine book positions."
    yellow_book_patch = yellow_book_patches[0]
    blue_book_patch = blue_book_patches[0]
    red_book_patch = red_book_patches[0]
    if yellow_book_patch.overlaps_with(blue_book_patch.left, blue_book_patch.lower, blue_book_patch.right, blue_book_patch.upper):
        return "The yellow book overlaps with the blue book."
    if yellow_book_patch.overlaps_with(red_book_patch.left, red_book_patch.lower, red_book_patch.right, red_book_patch.upper):
        return "The yellow book overlaps with the red book."
    if blue_book_patch.overlaps_with(red_book_patch.left, red_book_patch.lower, red_book_patch.right, red_book_patch.upper):
        return "The blue book overlaps with the red book."
    if yellow_book_patch.vertical_center > blue_book_patch.vertical_center or yellow_book_patch.vertical_center < red_book_patch.vertical_center:
        return "The yellow book is not between the blue and red books."
    return "The yellow book is above the blue book and below the red book."
answer = execute_command(image)