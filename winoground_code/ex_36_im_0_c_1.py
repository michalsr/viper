from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_36_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    chess_piece_patches = image_patch.find("metal chess piece")
    wood_patches = image_patch.find("wood")
    for chess_piece in chess_piece_patches:
        for wood in wood_patches:
            if chess_piece.overlaps_with(wood.left, wood.lower, wood.right, wood.upper):
                return "yes"
    return "no"
answer = execute_command(image)