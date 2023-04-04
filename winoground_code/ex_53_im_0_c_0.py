from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_53_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    if image_patch.exists("car") and image_patch.exists("dirt road"):
        car_patch = image_patch.find("car")[0]
        dirt_road_patch = image_patch.find("dirt road")[0]
        if car_patch.overlaps_with(dirt_road_patch.left, dirt_road_patch.lower, dirt_road_patch.right, dirt_road_patch.upper):
            return "no"
    return image_patch.llm_query("Is this a photo of driving off the road and on the unpaved terrain?")
answer = execute_command(image)