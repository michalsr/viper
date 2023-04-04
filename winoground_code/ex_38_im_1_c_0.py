from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_38_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.horizontal_center)
    if len(person_patches) < 2:
        return "Cannot determine the orientation of the people in the photo."
    happy_person = person_patches[-1]
    sad_person = person_patches[0]
    if happy_person.verify_property("person", "happy") and sad_person.verify_property("person", "sad"):
        if happy_person.horizontal_center > sad_person.horizontal_center:
            return "yes"
        else:
            return "no"
    else:
        return "Cannot determine the orientation of the people in the photo."
answer = execute_command(image)