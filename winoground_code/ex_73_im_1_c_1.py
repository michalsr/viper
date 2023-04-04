from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_73_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    watch_patches = image_patch.find("watch")
    if len(watch_patches) == 0:
        return "no"
    watch_patches.sort(key=lambda x: x.vertical_center)
    top_watch_patch = watch_patches[0]
    if top_watch_patch.vertical_center < image_patch.height / 2:
        return "yes"
    else:
        return "no"
answer = execute_command(image)