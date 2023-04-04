from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_5_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    bird_patches = image_patch.find("bird")
    snake_patches = image_patch.find("snake")
    if len(bird_patches) == 0 or len(snake_patches) == 0:
        return "no"
    else:
        bird_patch = bird_patches[0]
        snake_patch = snake_patches[0]
        if bird_patch.overlaps_with(snake_patch.left, snake_patch.lower, snake_patch.right, snake_patch.upper):
            return bird_patch.llm_query("Does this bird eat snakes?")
        else:
            return "no"
answer = execute_command(image)