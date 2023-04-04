from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_6_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    organism_patches = image_patch.find("organism")
    plant_patches = image_patch.find("plant")
    for organism in organism_patches:
        for plant in plant_patches:
            if organism.overlaps_with(plant.left, plant.lower, plant.right, plant.upper):
                return organism.llm_query("Was this organism harmed by the plant and broken into pieces?")
    return "No evidence of an organism being harmed by a plant in this photo."
answer = execute_command(image)