from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_76_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.vertical_center)
    person_patch = person_patches[0]
    kids_patches = image_patch.find("kids")
    kids_patches.sort(key=lambda x: x.vertical_center)
    kids_patch = kids_patches[0]
    if person_patch.horizontal_center < kids_patch.horizontal_center:
        return "no"
    else:
        return person_patch.llm_query("Is this a photo of me sitting with kids?")
answer = execute_command(image)