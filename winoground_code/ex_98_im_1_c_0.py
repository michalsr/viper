from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_98_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    vehicle_patches = image_patch.find("vehicle")
    person_patches.sort(key=lambda x: x.vertical_center)
    vehicle_patches.sort(key=lambda x: x.vertical_center)
    person_patch = person_patches[0]
    vehicle_patch = vehicle_patches[-1]
    if person_patch.vertical_center < vehicle_patch.vertical_center:
        return "no"
    else:
        water_patches = image_patch.find("water")
        water_patches.sort(key=lambda x: distance(x, person_patch))
        water_patch = water_patches[0]
        if water_patch.vertical_center < person_patch.vertical_center:
            return "no"
        else:
            return "yes" if distance(person_patch, vehicle_patch) < 0 else "no"
answer = execute_command(image)