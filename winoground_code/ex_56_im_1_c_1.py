from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_56_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    people_patches = image_patch.find("person")
    if len(people_patches) < 3:
        return "Not enough people in the photo to determine direction of movement."
    people_patches.sort(key=lambda x: x.horizontal_center)
    leftmost_person = people_patches[0]
    rightmost_person = people_patches[-1]
    middle_person = sorted(people_patches, key=lambda x: x.vertical_center)[1]
    if leftmost_person.horizontal_center < middle_person.horizontal_center < rightmost_person.horizontal_center:
        return "No, the people are not jumping towards the photographer and away from the others."
    elif leftmost_person.horizontal_center > middle_person.horizontal_center > rightmost_person.horizontal_center:
        return "Yes, the people are jumping towards the photographer and away from the others."
    else:
        return "Cannot determine direction of movement."
answer = execute_command(image)