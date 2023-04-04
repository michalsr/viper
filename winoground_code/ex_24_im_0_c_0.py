from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_24_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.compute_depth())
    if len(person_patches) < 2:
        return "Cannot determine the positions of the people in the photo."
    person_a = person_patches[0]
    person_b = person_patches[1]
    if person_a.horizontal_center < person_b.horizontal_center:
        weightlifter = person_a
        runner = person_b
    else:
        weightlifter = person_b
        runner = person_a
    if weightlifter.verify_property("person", "weightlifting") and runner.verify_property("person", "running"):
        return "Yes, the person closer to the camera weightlifts and the person farther from the camera runs."
    elif weightlifter.verify_property("person", "running") and runner.verify_property("person", "weightlifting"):
        return "Yes, the person closer to the camera runs and the person farther from the camera weightlifts."
    else:
        return "Cannot determine the positions of the people in the photo."
answer = execute_command(image)