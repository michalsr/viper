from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_95_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    hammer_patches = image_patch.find("hammer")
    hand_patches = image_patch.find("hand")
    for hammer in hammer_patches:
        for hand in hand_patches:
            if distance(hammer, hand) < 0:
                return "yes"
    return "no"
answer = execute_command(image)