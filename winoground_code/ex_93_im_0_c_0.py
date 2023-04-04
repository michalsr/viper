from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_93_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    boat_patches = image_patch.find("boat")
    if len(boat_patches) != 2:
        return "no"
    boat_patches.sort(key=lambda x: x.horizontal_center)
    if boat_patches[0].verify_property("boat", "upstream") or boat_patches[1].verify_property("boat", "downstream"):
        return "no"
    return image_patch.llm_query("Is this a photo of two boats and one direction down the stream?")
answer = execute_command(image)