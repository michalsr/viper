from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_31_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    red_book_patches = image_patch.find("red book")
    yellow_book_patches = image_patch.find("yellow book")
    blue_book_patches = image_patch.find("blue book")
    
    if len(red_book_patches) == 0 or len(yellow_book_patches) == 0 or len(blue_book_patches) == 0:
        return "Cannot answer the question as one or more books are missing from the image."
    
    red_book_patch = red_book_patches[0]
    yellow_book_patch = yellow_book_patches[0]
    blue_book_patch = blue_book_patches[0]
    
    # Check if red book is above yellow book
    if red_book_patch.vertical_center > yellow_book_patch.vertical_center:
        return "no"
    
    # Check if red book is below blue book
    if red_book_patch.vertical_center < blue_book_patch.vertical_center:
        return "no"
    
    # Check if yellow book is to the left of red book
    if yellow_book_patch.horizontal_center > red_book_patch.horizontal_center:
        return "no"
    
    # Check if blue book is to the right of red book
    if blue_book_patch.horizontal_center < red_book_patch.horizontal_center:
        return "no"
    
    return "yes"
answer = execute_command(image)