from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_44_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    heavy_traffic_patches = image_patch.find("heavy traffic")
    light_traffic_patches = image_patch.find("light traffic")
    if len(heavy_traffic_patches) == 0 or len(light_traffic_patches) == 0:
        return "Unable to determine if the photo shows heavy oncoming traffic contrasted with light outgoing traffic."
    heavy_traffic_patch = heavy_traffic_patches[0]
    light_traffic_patch = light_traffic_patches[0]
    if heavy_traffic_patch.vertical_center < light_traffic_patch.vertical_center:
        return "Yes, the photo shows heavy oncoming traffic contrasted with light outgoing traffic."
    else:
        return "No, the photo does not show heavy oncoming traffic contrasted with light outgoing traffic."
answer = execute_command(image)