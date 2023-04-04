from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_89_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    pink_person_patches = [person for person in person_patches if person.verify_property("person", "pink")]
    if not pink_person_patches:
        return "No pink person found in the image."
    pink_person_patch = pink_person_patches[0]
    left_of_pink_person_patches = [person for person in person_patches if person.horizontal_center < pink_person_patch.horizontal_center]
    if not left_of_pink_person_patches:
        return "No person found to the left of the pink person."
    left_of_pink_person_patch = max(left_of_pink_person_patches, key=lambda x: x.right)
    if left_of_pink_person_patch.right < pink_person_patch.left:
        return "The person in pink was not close to not winning."
    else:
        return "The person in pink was close to not winning."
answer = execute_command(image)