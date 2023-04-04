from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_5_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    snake_patches = image_patch.find("snake")
    bird_patches = image_patch.find("bird")
    if len(snake_patches) == 0 or len(bird_patches) == 0:
        return "no"
    else:
        snake_patch = snake_patches[0]
        bird_patch = bird_patches[0]
        if snake_patch.overlaps_with(bird_patch.left, bird_patch.lower, bird_patch.right, bird_patch.upper):
            return "yes"
        else:
            return "no"
answer = execute_command(image)