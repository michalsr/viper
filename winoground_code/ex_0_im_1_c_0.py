from image_patch import ImagePatch
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_0_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    people_patches = image_patch.find("person")
    if len(people_patches) < 2:
        return "no"
    people_patches.sort(key=lambda x: x.compute_depth())
    old_person_patch = people_patches[0]
    young_person_patch = people_patches[-1]
    if old_person_patch.horizontal_center < young_person_patch.horizontal_center:
        return old_person_patch.llm_query("Is this an old person kissing a young person?")
    else:
        return "no"
answer = execute_command(image)