from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_38_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.horizontal_center)
    if len(person_patches) < 2:
        return "Cannot determine the orientation of the people in the photo."
    else:
        left_person = person_patches[0]
        right_person = person_patches[-1]
        if left_person.verify_property("person", "happy") and right_person.verify_property("person", "sad"):
            return "Yes, the happy person is on the left and the sad person is on the right."
        elif left_person.verify_property("person", "sad") and right_person.verify_property("person", "happy"):
            return "Yes, the happy person is on the right and the sad person is on the left."
        else:
            return "Cannot determine the orientation of the people in the photo."
answer = execute_command(image)