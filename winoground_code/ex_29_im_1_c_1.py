from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_29_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    dog_patches = image_patch.find("dog")
    couch_patches = image_patch.find("couch")
    white_dog_patches = [dog for dog in dog_patches if dog.best_text_match(["white"]) == "white"]
    brown_couch_patches = [couch for couch in couch_patches if couch.best_text_match(["brown"]) == "brown"]
    if len(white_dog_patches) > 0 and len(brown_couch_patches) > 0:
        for dog in white_dog_patches:
            for couch in brown_couch_patches:
                if dog.overlaps_with(couch.left, couch.lower, couch.right, couch.upper):
                    return "yes"
        return "no"
    else:
        return "no information available"
answer = execute_command(image)