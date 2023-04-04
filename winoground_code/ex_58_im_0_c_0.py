from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_58_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    # Check if there is an egg in the image
    egg_exists = image_patch.exists("egg")
    # Check if there is a chicken in the image
    chicken_exists = image_patch.exists("chicken")
    # Check if there is a plate in the image
    plate_exists = image_patch.exists("plate")
    # Check if there is a fork in the image
    fork_exists = image_patch.exists("fork")
    # Check if there is a knife in the image
    knife_exists = image_patch.exists("knife")
    
    # If there is no egg or chicken, it cannot be a photo of it hatched before it was eaten
    if not egg_exists and not chicken_exists:
        return "no"
    # If there is no plate, fork, or knife, it cannot be a photo of it hatched before it was eaten
    if not plate_exists or not fork_exists or not knife_exists:
        return "no"
    
    # If there is an egg and a chicken, it is a photo of it hatched before it was eaten
    if egg_exists and chicken_exists:
        return "yes"
    
    # If there is only an egg, check if it is cracked
    egg_patches = image_patch.find("egg")
    for egg_patch in egg_patches:
        if egg_patch.verify_property("egg", "cracked"):
            return "no"
    
    # If there is only a chicken, check if it is cut
    chicken_patches = image_patch.find("chicken")
    for chicken_patch in chicken_patches:
        if chicken_patch.verify_property("chicken", "cut"):
            return "no"
    
    # If there is only an egg and it is not cracked, or only a chicken and it is not cut, it is a photo of it hatched before it was eaten
    return "yes"
answer = execute_command(image)