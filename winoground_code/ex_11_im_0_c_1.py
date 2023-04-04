from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_11_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    table_patches = image_patch.find("table")
    for table_patch in table_patches:
        below_table = table_patch.crop(table_patch.left, table_patch.upper, table_patch.right, table_patch.upper + 50)
        people_patches = below_table.find("person")
        if len(people_patches) > 0:
            return "yes"
    return "no"
answer = execute_command(image)