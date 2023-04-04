from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_34_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    rectangular_bushes = image_patch.find("rectangular bushes")
    pointy_bushes = image_patch.find("pointy bushes")
    if len(rectangular_bushes) == 0 or len(pointy_bushes) == 0:
        return "Cannot determine if rectangular bushes are behind pointy bushes."
    rectangular_bushes.sort(key=lambda x: x.compute_depth())
    pointy_bushes.sort(key=lambda x: x.compute_depth())
    if rectangular_bushes[0].vertical_center > pointy_bushes[-1].vertical_center:
        return "Yes, rectangular bushes are behind pointy bushes."
    else:
        return "No, rectangular bushes are not behind pointy bushes."
answer = execute_command(image)