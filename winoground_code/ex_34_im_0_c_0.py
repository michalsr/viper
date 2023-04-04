from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_34_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    pointy_bushes = image_patch.find("pointy bushes")
    rectangular_bushes = image_patch.find("rectangular bushes")
    if pointy_bushes and rectangular_bushes:
        pointy_bushes.sort(key=lambda x: x.horizontal_center)
        rectangular_bushes.sort(key=lambda x: x.horizontal_center)
        if pointy_bushes[0].horizontal_center < rectangular_bushes[0].horizontal_center:
            return "yes"
        else:
            return "no"
    else:
        return image_patch.llm_query("Are there pointy bushes behind rectangular bushes in this photo?")
answer = execute_command(image)