from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_78_img_1.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    # Check if there is a person in the image
    if not image_patch.exists("person"):
        return "no"
    # Check if there is a tree with an apple in the image
    tree_patches = image_patch.find("tree")
    for tree_patch in tree_patches:
        if tree_patch.best_text_match(["apple"]) == "apple":
            # Check if the person overlaps with the tree
            person_patches = image_patch.find("person")
            for person_patch in person_patches:
                if person_patch.overlaps_with(tree_patch.left, tree_patch.lower, tree_patch.right, tree_patch.upper):
                    return "yes"
    return "no"
answer = execute_command(image)