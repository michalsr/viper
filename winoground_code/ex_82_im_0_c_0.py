from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_82_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.horizontal_center)
    curly_patch = person_patches[0]
    straight_patch = person_patches[1]
    curly_hair = curly_patch.simple_query("What is the hair type?")
    straight_hair = straight_patch.simple_query("What is the hair type?")
    patterned_shirt = None
    for person_patch in person_patches:
        if person_patch.verify_property("person", "patterned shirt"):
            patterned_shirt = person_patch
            break
    if patterned_shirt is None:
        return "No person with a patterned shirt found in the image."
    curly_patterned = patterned_shirt.overlaps_with(curly_patch.left, curly_patch.lower, curly_patch.right, curly_patch.upper)
    straight_patterned = patterned_shirt.overlaps_with(straight_patch.left, straight_patch.lower, straight_patch.right, straight_patch.upper)
    if curly_patterned and not straight_patterned and curly_hair == "curly":
        return "yes"
    elif straight_patterned and not curly_patterned and straight_hair == "straight":
        return "yes"
    else:
        return "no"
answer = execute_command(image)