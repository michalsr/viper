from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_51_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.compute_depth())
    if len(person_patches) == 0:
        return "no"
    person_patch = person_patches[0]
    water_patches = image_patch.find("water")
    sand_patches = image_patch.find("sand")
    for water_patch in water_patches:
        for sand_patch in sand_patches:
            if person_patch.overlaps_with(water_patch.left, sand_patch.lower, water_patch.right, sand_patch.upper):
                return "yes"
    return "no"
answer = execute_command(image)