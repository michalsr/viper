from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_33_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    table_patches = image_patch.find("table")
    for table_patch in table_patches:
        if table_patch.verify_property("table", "square") and table_patch.best_text_match(["round"]) == "round":
            return "yes"
    return "no"
answer = execute_command(image)