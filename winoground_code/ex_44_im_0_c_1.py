from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_44_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    # Check if there are any traffic lights in the image
    if not image_patch.exists("traffic light"):
        return "No traffic lights found in the image."
    # Check if there is heavy outgoing traffic
    heavy_traffic_patches = image_patch.find("heavy traffic")
    if not heavy_traffic_patches:
        return "No heavy outgoing traffic found in the image."
    # Check if there is light oncoming traffic
    light_traffic_patches = image_patch.find("light traffic")
    if not light_traffic_patches:
        return "No light oncoming traffic found in the image."
    # Sort traffic patches by vertical center
    heavy_traffic_patches.sort(key=lambda x: x.vertical_center)
    light_traffic_patches.sort(key=lambda x: x.vertical_center)
    # Check if the light traffic is above the heavy traffic
    if light_traffic_patches[0].vertical_center < heavy_traffic_patches[-1].vertical_center:
        return "Yes, this is a photo of the light oncoming traffic contrasted with the heavy outgoing traffic."
    else:
        return "No, this is not a photo of the light oncoming traffic contrasted with the heavy outgoing traffic."
answer = execute_command(image)