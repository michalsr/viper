from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_93_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    boat_patches = image_patch.find("boat")
    if len(boat_patches) != 1:
        return "no"
    boat_patch = boat_patches[0]
    stream_patches = image_patch.find("stream")
    if len(stream_patches) != 2:
        return "no"
    stream_patches.sort(key=lambda x: x.vertical_center)
    if boat_patch.vertical_center > stream_patches[1].vertical_center:
        return "no"
    return "yes"
answer = execute_command(image)