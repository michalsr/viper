from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_47_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    sailboat_patches = image_patch.find("sailboat")
    sailboat_patch = sailboat_patches[0]
    beach_patches = image_patch.find("beach")
    beach_patch = beach_patches[0]
    if sailboat_patch.vertical_center > beach_patch.vertical_center:
        return "no"
    else:
        distance_to_sailboat = distance(sailboat_patch, image_patch)
        distance_to_beach = distance(beach_patch, image_patch)
        if distance_to_sailboat < distance_to_beach:
            return "yes"
        else:
            return "no"
answer = execute_command(image)