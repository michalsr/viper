from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_49_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    hat_patches = image_patch.find("hat")
    person_patches = image_patch.find("person")
    if len(hat_patches) > 0 and len(person_patches) > 0:
        for hat_patch in hat_patches:
            for person_patch in person_patches:
                if hat_patch.overlaps_with(person_patch.left, person_patch.lower, person_patch.right, person_patch.upper):
                    return "no"
        return "yes"
    else:
        return image_patch.llm_query("What is this a photo of?")
answer = execute_command(image)