import sys 
sys.path.append('/home/michal5/viper')
from image_patch import ImagePatch

def object_loc(image,subject,question):
    #includes image size 
    image_patch = ImagePatch(image)
    subject_patch = image_patch.find_center(subject)
    image_center_x = int(image_patch.width/2)
    image_center_y = int(image_patch.height/2)
    if subject_patch.center[0] < image_center_x:
        x_position= 'left'
    else:
        x_position = 'right'
    if subject_patch.center[1] <image_center_y:
        y_position = 'top'
    else:
        y_position = 'bottom'

    if 'left' in question and 'right' not in question:
        if x_position == 'left':
            return 'yes'
        else:
            return 'no'
    if  'right' in question and 'left' not in question:
        if x_position == 'right':
            return 'yes'
        else:
            return 'no'
    if 'right' in question and 'left' in question:
        return x_position
    if 'top' in question and 'bottom' not in question:
        if y_position == 'top':
            return 'yes'
        else:
            return 'no'
    if  'bottom' in question and 'top' not in question:
        if y_position == 'bottom':
            return 'yes'
        else:
            return 'no'
    if 'bottom' in question and 'top' in question:
        return y_position
