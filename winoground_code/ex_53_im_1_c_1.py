from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_53_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    road_patches = image_patch.find("road")
    unpaved_patches = image_patch.find("unpaved terrain")
    if len(road_patches) > 0 and len(unpaved_patches) > 0:
        road_patch = road_patches[0]
        unpaved_patch = unpaved_patches[0]
        if road_patch.vertical_center > unpaved_patch.vertical_center:
            return "yes"
        else:
            return "no"
    else:
        return image_patch.llm_query("Is this a photo of driving on the road and off the unpaved terrain?")
answer = execute_command(image)