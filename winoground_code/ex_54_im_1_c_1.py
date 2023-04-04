from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_54_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    helicopter_patches = image_patch.find("helicopter")
    car_patches = image_patch.find("car")
    person_patches = image_patch.find("person")
    if len(helicopter_patches) > 0 and len(car_patches) > 0 and len(person_patches) > 0:
        for person_patch in person_patches:
            for helicopter_patch in helicopter_patches:
                for car_patch in car_patches:
                    if person_patch.overlaps_with(car_patch.left, car_patch.lower, car_patch.right, car_patch.upper) and person_patch.overlaps_with(helicopter_patch.left, helicopter_patch.lower, helicopter_patch.right, helicopter_patch.upper):
                        return "yes"
    return image_patch.llm_query("Is this a photo of someone with a helicopter in a car?")
answer = execute_command(image)