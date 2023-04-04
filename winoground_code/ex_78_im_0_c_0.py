from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_78_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    person_patches = image_patch.find("person")
    apple_patches = image_patch.find("apple")
    tree_patches = image_patch.find("tree")
    
    if len(person_patches) == 0 or len(apple_patches) == 0 or len(tree_patches) == 0:
        return "Cannot answer the question as one or more objects are missing from the image."
    
    person_patch = person_patches[0]
    apple_patch = apple_patches[0]
    tree_patch = tree_patches[0]
    
    if person_patch.overlaps_with(apple_patch.left, apple_patch.lower, apple_patch.right, apple_patch.upper):
        if person_patch.overlaps_with(tree_patch.left, tree_patch.lower, tree_patch.right, tree_patch.upper):
            return "Yes, the photo shows a person with an apple being hurt by a tree."
        else:
            return "No, the photo shows a person with an apple but not being hurt by a tree."
    else:
        return "No, the photo does not show a person with an apple being hurt by a tree."
answer = execute_command(image)