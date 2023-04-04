from image_patch import ImagePatch
from image_patch import distance
from PIL import Image
image = Image.open('/home/michal5/winoground/data/images/ex_65_img_0.png').convert('RGB')
def execute_command(image) -> str:
    image_patch = ImagePatch(image)
    animal_patches = image_patch.find("animal")
    person_patches = image_patch.find("person")
    if len(animal_patches) == 0 or len(person_patches) == 0:
        return "Cannot answer the question as either the animal or person is not present in the image."
    animal_patch = animal_patches[0]
    person_patch = person_patches[0]
    animal_eye_patches = animal_patch.find("eye")
    person_eye_patches = person_patch.find("eye")
    if len(animal_eye_patches) == 0 or len(person_eye_patches) == 0:
        return "Cannot answer the question as either the animal or person does not have visible eyes in the image."
    animal_eye_patch = animal_eye_patches[0]
    person_eye_patch = person_eye_patches[0]
    animal_eye_size = animal_eye_patch.width * animal_eye_patch.height
    person_eye_size = person_eye_patch.width * person_eye_patch.height
    if animal_eye_size > person_eye_size:
        return "yes"
    elif animal_eye_size < person_eye_size:
        return "no"
    else:
        return "Cannot answer the question as the size of the animal's and person's eyes are the same."
answer = execute_command(image)