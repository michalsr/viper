from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_24_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.compute_depth())
    if len(person_patches) < 2:
        return "Cannot determine from the image."
    closer_person = person_patches[0]
    farther_person = person_patches[1]
    if closer_person.verify_property("person", "running") and farther_person.verify_property("person", "weightlifting"):
        return "Yes"
    elif closer_person.verify_property("person", "weightlifting") and farther_person.verify_property("person", "running"):
        return "Yes"
    else:
        return "No"
answer = execute_command(image)