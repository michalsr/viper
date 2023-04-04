from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_54_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    helicopter_patches = image_patch.find("helicopter")
    car_patches = image_patch.find("car")
    if len(helicopter_patches) > 0 and len(car_patches) > 0:
        for helicopter_patch in helicopter_patches:
            for car_patch in car_patches:
                if distance(helicopter_patch, car_patch) < 0:
                    return "yes"
    return image_patch.llm_query("Is this a photo of someone in a helicopter with a car?")
answer = execute_command(image)