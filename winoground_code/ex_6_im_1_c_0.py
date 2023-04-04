from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_6_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    plant_patches = image_patch.find("plant")
    for plant_patch in plant_patches:
        if plant_patch.exists("broken") and plant_patch.exists("pieces"):
            if plant_patch.exists("harmed") and plant_patch.exists("organism"):
                return "Yes, this is a photo of a plant that was harmed by another organism and broken into pieces."
            else:
                return "No, this is a photo of a plant that was broken into pieces, but there is no evidence of harm by another organism."
    return "No, this is not a photo of a plant that was broken into pieces."
answer = execute_command(image)