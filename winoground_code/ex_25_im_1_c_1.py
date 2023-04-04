from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_25_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    white_shirt_patches = [person for person in person_patches if person.verify_property("person", "white collared shirt")]
    plant_patches = image_patch.find("plant")
    watering_can_patches = image_patch.find("watering can")
    
    for person_patch in white_shirt_patches:
        for plant_patch in plant_patches:
            if person_patch.overlaps_with(plant_patch.left, plant_patch.lower, plant_patch.right, plant_patch.upper):
                for watering_can_patch in watering_can_patches:
                    if watering_can_patch.overlaps_with(plant_patch.left, plant_patch.lower, plant_patch.right, plant_patch.upper):
                        return "yes"
    return "no"
answer = execute_command(image)