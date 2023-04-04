from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_69_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    people_patches = image_patch.find("person")
    boat_patches = image_patch.find("boat")
    if len(people_patches) > 1 and len(boat_patches) == 1:
        people_patches.sort(key=lambda x: x.compute_depth())
        boat_patch = boat_patches[0]
        if people_patches[0].overlaps_with(boat_patch.left, boat_patch.lower, boat_patch.right, boat_patch.upper):
            return "yes"
    return "no"
answer = execute_command(image)