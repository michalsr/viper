from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_11_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    table_patches = image_patch.find("table")
    person_patches = image_patch.find("person")
    for person in person_patches:
        for table in table_patches:
            if person.vertical_center > table.vertical_center:
                return "yes"
    return "no"
answer = execute_command(image)