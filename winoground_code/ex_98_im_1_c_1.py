from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_98_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    vehicle_patches = image_patch.find("vehicle")
    person_patches = image_patch.find("person")
    water_patches = image_patch.find("water")
    for vehicle in vehicle_patches:
        for person in person_patches:
            if person.vertical_center > vehicle.vertical_center:
                for water in water_patches:
                    if water.overlaps_with(vehicle.left, vehicle.lower, vehicle.right, vehicle.upper):
                        return "yes"
    return "no"
answer = execute_command(image)