from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_27_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_with_ponytail = None
    for person in person_patches:
        if person.verify_property("person", "ponytail"):
            person_with_ponytail = person
            break
    if person_with_ponytail is None:
        return "No"
    else:
        left = person_with_ponytail.left
        right = person_with_ponytail.right
        upper = person_with_ponytail.upper
        lower = person_with_ponytail.lower
        stuff_patches = image_patch.find("stuff")
        buys_patches = image_patch.find("buys")
        for patch in stuff_patches + buys_patches:
            if patch.overlaps_with(left, lower, right, upper):
                return "Yes"
        return "No"
answer = execute_command(image)