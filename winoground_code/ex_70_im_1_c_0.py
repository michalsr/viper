from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_70_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    lighter_shoe_patches = image_patch.find("lighter shoes")
    darker_shoe_patches = image_patch.find("darker shoes")
    lighter_shoe_patch = lighter_shoe_patches[0]
    darker_shoe_patch = darker_shoe_patches[0]
    lighter_shoe_center = (lighter_shoe_patch.horizontal_center, lighter_shoe_patch.vertical_center)
    darker_shoe_center = (darker_shoe_patch.horizontal_center, darker_shoe_patch.vertical_center)
    if lighter_shoe_center[1] < darker_shoe_center[1]:
        person_with_emoji_patch = lighter_shoe_patch
        person_without_emoji_patch = darker_shoe_patch
    else:
        person_with_emoji_patch = darker_shoe_patch
        person_without_emoji_patch = lighter_shoe_patch
    emoji_patches = person_with_emoji_patch.find("emoji")
    if len(emoji_patches) > 0 and person_without_emoji_patch.verify_property("person", "holding nothing"):
        return "yes"
    else:
        return "no"
answer = execute_command(image)