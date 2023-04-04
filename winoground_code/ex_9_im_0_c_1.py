from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_9_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    # Check if the image contains people
    if not image_patch.exists("people"):
        return "No, there are no people in the photo."
    # Check if the image contains leaves
    if not image_patch.exists("leaves"):
        return "No, there are no leaves in the photo."
    # Check if the leaves are falling on the people
    people_patches = image_patch.find("people")
    leaf_patches = image_patch.find("leaves")
    for leaf_patch in leaf_patches:
        for person_patch in people_patches:
            if leaf_patch.overlaps_with(person_patch.left, person_patch.lower, person_patch.right, person_patch.upper):
                return "Yes, this is a photo of leaves falling on people."
    return "No, the leaves are not falling on the people in the photo."
answer = execute_command(image)