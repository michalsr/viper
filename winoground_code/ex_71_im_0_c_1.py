from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_71_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    person_patches.sort(key=lambda x: x.horizontal_center)
    if len(person_patches) < 2:
        return "No, there is not enough people in the photo."
    person1_patch = person_patches[0]
    person2_patch = person_patches[1]
    if person1_patch.verify_property("person", "bright colors") and person2_patch.verify_property("person", "neutral colors"):
        return "Yes, the person wearing brighter colors poses and the person wearing neutral colors takes a picture."
    elif person2_patch.verify_property("person", "bright colors") and person1_patch.verify_property("person", "neutral colors"):
        return "Yes, the person wearing brighter colors poses and the person wearing neutral colors takes a picture."
    else:
        return "No, the people in the photo are not wearing distinct enough colors to determine who is posing and who is taking the picture."
answer = execute_command(image)