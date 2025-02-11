from __future__ import annotations
from statistics import mean
import numpy as np
import re
import torch
from dateutil import parser as dateparser
from PIL import Image
from rich.console import Console
import torchvision
from torchvision import transforms
from torchvision.ops import box_iou
from typing import Union, List
from PIL import ImageDraw 
from word2number import w2n
import numpy as np
from utils import show_single_image, load_json
from vision_processes import forward, config

console = Console(highlight=False)
ABOVE_WORDS = ['above','higher','on top',]
BELOW_WORDS = ['below','lower','under','underneath']


class ImagePatch:
    """A Python class containing a crop of an image centered around a particular object, as well as relevant
    information.
    Attributes
    ----------
    cropped_image : array_like
        An array-like of the cropped image taken from the original image.
    left : int
        An int describing the position of the left border of the crop's bounding box in the original image.
    lower : int
        An int describing the position of the bottom border of the crop's bounding box in the original image.
    right : int
        An int describing the position of the right border of the crop's bounding box in the original image.
    upper : int
        An int describing the position of the top border of the crop's bounding box in the original image.

    Methods
    -------
    find(object_name: str)->List[ImagePatch]
        Returns a list of new ImagePatch objects containing crops of the image centered around any objects found in the
        image matching the object_name.
    exists(object_name: str)->bool
        Returns True if the object specified by object_name is found in the image, and False otherwise.
    verify_property(property: str)->bool
        Returns True if the property is met, and False otherwise.
    best_text_match(option_list: List[str], prefix: str)->str
        Returns the string that best matches the image.
    simple_query(question: str=None)->str
        Returns the answer to a basic question asked about the image. If no question is provided, returns the answer
        to "What is this?".
    compute_depth()->float
        Returns the median depth of the image crop.
    crop(left: int, lower: int, right: int, upper: int)->ImagePatch
        Returns a new ImagePatch object containing a crop of the image at the given coordinates.
    """

    def __init__(self, image: Union[Image.Image, torch.Tensor, np.ndarray], left: int = None, lower: int = None,
                 right: int = None, upper: int = None,parent_left=0, parent_lower=0, confidence: float = 1.0,queues=None,
                 parent_img_patch=None):
        """Initializes an ImagePatch object by cropping the image at the given coordinates and stores the coordinates as
        attributes. If no coordinates are provided, the image is left unmodified, and the coordinates are set to the
        dimensions of the image.

        Parameters
        -------
        image : array_like
            An array-like of the original image.
        left : int
            An int describing the position of the left border of the crop's bounding box in the original image.
        lower : int
            An int describing the position of the bottom border of the crop's bounding box in the original image.
        right : int
            An int describing the position of the right border of the crop's bounding box in the original image.
        upper : int
            An int describing the position of the top border of the crop's bounding box in the original image.

        """
        #console.print('I imported')
        if isinstance(image, Image.Image):
            image = transforms.ToTensor()(image)
        elif isinstance(image, np.ndarray):
            image = torch.tensor(image).permute(1, 2, 0)
        elif isinstance(image, torch.Tensor) and image.dtype == torch.uint8:
            image = image / 255
        
        if left is None and right is None and upper is None and lower is None:
            self.cropped_image = image
            self.left = 0
            self.lower = 0
      
            self.right = image.shape[2]  # width
            self.upper = image.shape[1]  # height
            self.confidence = 1.0
        else:
            self.cropped_image = image
            self.left = left + parent_left
            self.upper = upper + parent_lower
            self.right = right + parent_left
            self.lower = lower + parent_lower
            self.confidence = confidence 

        self.height = self.cropped_image.shape[1]
        self.width = self.cropped_image.shape[2]
        self.score = 1.0
        self.cache = {}
        self.queues = (None, None) if queues is None else queues

        self.parent_img_patch = parent_img_patch
        
        self.horizontal_center = (self.left + self.right) / 2
        self.vertical_center = (self.lower + self.upper) / 2
        self.center = None 
        if self.cropped_image.shape[1] == 0 or self.cropped_image.shape[2] == 0:
            raise Exception("ImagePatch has no area")

        self.possible_options = load_json('./useful_lists/possible_options.json')

    def forward(self, model_name, *args, **kwargs):
        return forward(model_name, *args, queues=self.queues, **kwargs)

    @property
    def original_image(self):
        if self.parent_img_patch is None:
            return self.cropped_image
        else:
            return self.parent_img_patch.original_image
    def location_short(self,object_1_name,object_2_name,object_1_coords,object_2_coords,image_height,image_width):
        return f"In an image pixels in the vertical direction increase from top to bottom and in the horizontal direction increase from left to right. The horizontal and vertical center of {object_1_name}'s bounding box is at {object_1_coords} and the horizontal and vertical center of {object_2_name}'s bounding box is at {object_2_coords}."
    def location_template(self,object_1_name,object_2_name,object_1_coords,object_2_coords,image_height,image_width):
        return f"In an image of height {image_height} and width {image_width} pixels in the vertical direction increase from top to bottom and in the horizontal direction increase from left to right. The horizontal and vertical center of {object_1_name}'s bounding box is at {object_1_coords} and the horizontal and vertical center of {object_2_name}'s bounding box is at {object_2_coords}."
    def location_template_relate(self,object_1_name,object_2_name,object_1_coords,object_2_coords,relate,image_height,image_width):
        return f"In an image of height {image_height} and width {image_width} pixels in the vertical direction increase from top to bottom and in the horizontal direction increase from left to right. The horizontal and vertical center of {object_1_name}'s bounding box is at {object_1_coords} and the horizontal and vertical center of {object_2_name}'s bounding box is at {object_2_coords}. Is {object_1_name} {relate} {object_2_name}?"

    def find_center(self,object_name:str):
        #console.print('Running GLIP')
        #print(object_name,'object nane')
        results = []
        #print(object_name,'object name')
        # if object_name in ["object", "objects"]:
        #     all_object_coordinates = self.forward('maskrcnn', self.cropped_image)[0]
        # else:

        #     if object_name == 'person':
        #         object_name = 'people'  # GLIP does better at people than person
            
        all_object_coordinates, scores = self.forward('owlvit', self.cropped_image, object_name)
        #print('second scores',scores)
        #     #console.print('GLIP finished running')
        # if len(all_object_coordinates) == 0:
        #     return []
       
        #scores torch.unsqueeze(scores,1)
        #print(scores[:5],scores.size())
        
        #ßßprint(scores,'scores')
        _,top_idx= torch.topk(scores,1)

        #print(top_idx)
        coords = all_object_coordinates[top_idx.long()][0]
       
        scores = scores[top_idx.long()]
        #print(len(scores),'scores')
        #boxes_on_image = self.draw_boxes(all_object_coordinates)
        new_image_patch = self.crop(left=coords[0],lower=coords[1],right=coords[2],upper=coords[3],confidence=1)
        new_image_patch.score = scores
        h_c = int((coords[0]+coords[2])/2)
        h_b = int((coords[1]+coords[3])/2)
        new_image_patch.center = (h_c,h_b)
        #print(coords[0],coords[1],coords[2],coords[3],'coords')
        return new_image_patch
    def find(self,object_name,k=-1):
        threshold = config.ratio_box_area_to_image_area
        all_object_coordinates, scores = self.forward('owlvit', self.cropped_image, object_name)
        new_objects = []
        if threshold > 0:
            area_im = self.width * self.height
            all_areas = torch.tensor([(coord[2]-coord[0]) * (coord[3]-coord[1]) / area_im
                                      for coord in all_object_coordinates])
            mask = all_areas > threshold
            # if not mask.any():
            #     mask = all_areas == all_areas.max()  # At least return one element
            all_object_coordinates = all_object_coordinates[mask]
        if k>-1:
            if len(scores) > k:
                _,top_idx= torch.topk(scores,k=k)
                all_object_coordinates = all_object_coordinates[top_idx.long()]
            
        for obj in all_object_coordinates:
            new_obj = self.crop(left=obj[0],lower=obj[1],right=obj[2],upper=obj[3],confidence=1)
            h_c = int((obj[0]+obj[2])/2)
            h_b = int((obj[1]+obj[3])/2)
            new_obj.center = (h_c,h_b)
            new_objects.append(new_obj)
            




        return new_objects
    def find_one(self, object_name: str) -> list[ImagePatch]:
        """Returns a list of ImagePatch objects matching object_name contained in the crop if any are found.
        Otherwise, returns an empty list.
        Parameters
        ----------
        object_name : str
            the name of the object to be found

        Returns
        -------
        List[ImagePatch]
            a list of ImagePatch objects matching object_name contained in the crop
        """
        #console.print('Running GLIP')
        #print(object_name,'object nane')
        results = []
        #print(object_name,'object name')
        # if object_name in ["object", "objects"]:
        #     all_object_coordinates = self.forward('maskrcnn', self.cropped_image)[0]
        # else:

        #     if object_name == 'person':
        #         object_name = 'people'  # GLIP does better at people than person
            
        all_object_coordinates, scores = self.forward('owlvit', self.cropped_image, object_name)
        #print('second scores',scores)
        #     #console.print('GLIP finished running')
        # if len(all_object_coordinates) == 0:
        #     return []
       
        #scores torch.unsqueeze(scores,1)
        #print(scores[:5],scores.size())
        
        #ßßprint(scores,'scores')
        _,top_idx= torch.topk(scores,1)

        #print(top_idx)
        coords = all_object_coordinates[top_idx.long()][0]
       
        scores = scores[top_idx.long()]
        #print(len(scores),'scores')
        #boxes_on_image = self.draw_boxes(all_object_coordinates)
        new_image_patch = self.crop(left=coords[0],lower=coords[1],right=coords[2],upper=coords[3],confidence=1)
        h_c = int((coords[0]+coords[2])/2)
        h_b = int((coords[1]+coords[3])/2)
        new_image_patch.score = scores
        #print(coords[0],coords[1],coords[2],coords[3],'coords')
        #new_image_patch = ImagePatch(boxes_on_image)
        #results = [new_image_patch]
        #torchvision.utils.save_image(new_image_patch.cropped_image,'/home/michal5/viper/person.jpg')

        #all_object_coordinates, scores = all_object_coordinates[top_idx.long()], scores[top_idx.long()]
        #print(len(all_object_coordinates),'all object coordinates')
        #print(len(scores),'scores')
        # for coords, score in zip(all_object_coordinates,scores):
        #     results.append(self.crop(left=coords[0],lower=coords[1],right=coords[2],upper=coords[3],confidence=score))
        # # threshold = config.ratio_box_area_to_image_area
        # if threshold > 0:
        #     area_im = self.width * self.height
        #     all_areas = torch.tensor([(coord[2]-coord[0]) * (coord[3]-coord[1]) / area_im
        #                               for coord in all_object_coordinates])
        #     mask = all_areas > threshold
        #     # if not mask.any():
        #     #     mask = all_areas == all_areas.max()  # At least return one element
        #     all_object_coordinates = all_object_coordinates[mask]
        #print(h_c,h_b,'c,b')
        return new_image_patch
        #return results,np.mean(scores.tolist())
    
    def draw_boxes(self,coords):
        pil_transform = transforms.ToPILImage()
        img_to_draw = pil_transform(self.cropped_image)
        draw = ImageDraw.Draw(img_to_draw)
        for c in coords:
            x_1,y_1,x_2,y_2 = c
            new_c = [int((x_1.item()+x_2.item())/2),int((y_1.item()+y_2.item())/2),x_2.item(),y_2.item()]

            # c = c.tolist()
            draw.ellipse(new_c,outline='red',width=2)
        return img_to_draw
    def exists(self, object_name) -> bool:
        """Returns True if the object specified by object_name is found in the image, and False otherwise.
        Parameters
        -------
        object_name : str
            A string describing the name of the object to be found in the image.
        """
        if object_name.isdigit() or object_name.lower().startswith("number"):
            object_name = object_name.lower().replace("number", "").strip()

            object_name = w2n.word_to_num(object_name)
            answer = self.simple_query("What number is written in the image (in digits)?")
            return w2n.word_to_num(answer) == object_name

        patches = self.find(object_name)
        patch_confidence = []
        filtered_patches = []
        for patch in patches:
            if "yes" in patch.simple_query(f"Is this a {object_name}?"):
                filtered_patches.append(patch)
                patch_confidence.append(patch.confidence.item())
        return np.mean(patch_confidence)

    def _score(self, category: str, negative_categories=None, model='clip') -> float:
        """
        Returns a binary score for the similarity between the image and the category.
        The negative categories are used to compare to (score is relative to the scores of the negative categories).
        """
        if model == 'clip':
            res = self.forward('clip', self.cropped_image, category, task='score',
                               negative_categories=negative_categories)
        elif model == 'tcl':
            res = self.forward('tcl', self.cropped_image, category, task='score')
        else:  # xvlm
            task = 'binary_score' if negative_categories is not None else 'score'
            res = self.forward('xvlm', self.cropped_image, category, task=task, negative_categories=negative_categories)
            res = res.item()

        return res

    def _detect(self, category: str, thresh, negative_categories=None, model='clip') -> float:
        return self._score(category, negative_categories, model) 

    def verify_property(self, object_name: str, attribute: str) -> bool:
        """Returns True if the object possesses the property, and False otherwise.
        Differs from 'exists' in that it presupposes the existence of the object specified by object_name, instead
        checking whether the object possesses the property.
        Parameters
        -------
        object_name : str
            A string describing the name of the object to be found in the image.
        attribute : str
            A string describing the property to be checked.
        """
        name = f"{attribute} {object_name}"
        model = config.verify_property.model
        negative_categories = [f"{att} {object_name}" for att in self.possible_options['attributes']]
        return self._detect(name, negative_categories=negative_categories,
                                thresh=config.verify_property.thresh_clip, model='clip')
        if model == 'clip':
            return self._detect(name, negative_categories=negative_categories,
                                thresh=config.verify_property.thresh_clip, model='clip')
        elif model == 'tcl':
            return self._detect(name, thresh=config.verify_property.thresh_tcl, model='tcl')
        else:  # 'xvlm'
            return self._detect(name, negative_categories=negative_categories,
                                thresh=config.verify_property.thresh_xvlm, model='xvlm')

    def best_text_match(self, option_list: list[str] = None, prefix: str = None) -> str:
        """Returns the string that best matches the image.
        Parameters
        -------
        option_list : str
            A list with the names of the different options
        prefix : str
            A string with the prefixes to append to the options
        """
        option_list_to_use = option_list
        if prefix is not None:
            option_list_to_use = [prefix + " " + option for option in option_list]

        model_name = 'clip'
        image = self.cropped_image
        text = option_list_to_use
        # if model_name in ('clip', 'tcl'):
        #     selected = self.forward(model_name, image, text, task='classify')
        # elif model_name == 'xvlm':
        #     res = self.forward(model_name, image, text, task='score')
        #     res = res.argmax().item()
        #     selected = res
        # else:
        #     raise NotImplementedError
        selected = self.forward(model_name, image, text, task='classify')
        # res = res.argmax().item()
        # selected = res
        return option_list[selected]

    def simple_query(self, question: str):
        """Returns the answer to a basic question asked about the image. If no question is provided, returns the answer
        to "What is this?". The questions are about basic perception, and are not meant to be used for complex reasoning
        or external knowledge.
        Parameters
        -------
        question : str
            A string describing the question to be asked.
        """
        #console.print('Running BLIP')
        return self.forward('blip', self.cropped_image, question=question,task='qa')
    
    def compute_depth(self):
        """Returns the median depth of the image crop
        Parameters
        ----------
        Returns
        -------
        float
            the median depth of the image crop
        """
        original_image = self.original_image
        #console.print('Running depth')
        depth_map = self.forward('depth', original_image)
        depth_map = depth_map[original_image.shape[1]-self.upper:original_image.shape[1]-self.lower,
                              self.left:self.right]
        return depth_map.median()  # Ideally some kind of mode, but median is good enough for now

    def crop(self, left: int, lower: int, right: int, upper: int, confidence=1) -> ImagePatch:
        """Returns a new ImagePatch containing a crop of the original image at the given coordinates.
        Parameters
        ----------
        left : int
            the position of the left border of the crop's bounding box in the original image
        lower : int
            the position of the bottom border of the crop's bounding box in the original image
        right : int
            the position of the right border of the crop's bounding box in the original image
        upper : int
            the position of the top border of the crop's bounding box in the original image
        confidence : float
            the score returned from model 
        Returns
        -------
        ImagePatch
            a new ImagePatch containing a crop of the original image at the given coordinates
        """
        # make all inputs ints
        left = int(left)
        lower = int(lower)
        right = int(right)
        upper = int(upper)

        # if config.crop_larger_margin:
        #     left = max(0, left - 10)
        #     lower = max(0, lower - 10)
        #     right = min(self.width, right + 10)
        #     upper = min(self.height, upper + 10)
        #.print('Cropping')
        return ImagePatch(self.cropped_image, left, lower, right, upper, self.left, self.lower, queues=self.queues,
                          parent_img_patch=None,confidence=confidence)
    def overlaps_with(self, left, lower, right, upper):
        """Returns True if a crop with the given coordinates overlaps with this one,
        else False.
        Parameters
        ----------
        left : int
            the left border of the crop to be checked
        lower : int
            the lower border of the crop to be checked
        right : int
            the right border of the crop to be checked
        upper : int
            the upper border of the crop to be checked
        Returns
        -------
        bool
            True if a crop with the given coordinates overlaps with this one, else False
        """
        return self.left <= right and self.right >= left and self.lower <= upper and self.upper >= lower
    # def overlaps_with(self, image_2):
    #     """Returns True if a crop with the given coordinates overlaps with this one,
    #     else False.
    #     Parameters
    #     ----------
    #     left : int
    #         the left border of the crop to be checked
    #     lower : int
    #         the lower border of the crop to be checked
    #     right : int
    #         the right border of the crop to be checked
    #     upper : int
    #         the upper border of the crop to be checked

    #     Returns
    #     -------
    #     bool
    #         True if a crop with the given coordinates overlaps with this one, else False
    #     """
    #     right = image_2.right
    #     left = image_2.left
    #     upper = image_2.upper
    #     lower = image_2.lower
    #     return self.left <= right and self.right >= left and self.lower <= upper and self.upper >= lower

    def llm_query(self, question: str, long_answer: bool = True) -> str:
        #console.print('Querying')
        return llm_query(question, None, long_answer)

    def print_image(self, size: tuple[int, int] = None):
        show_single_image(self.cropped_image, size)

    def __repr__(self):
        return "ImagePatch({}, {}, {}, {})".format(self.left, self.lower, self.right, self.upper)


def best_image_match(list_patches: list[ImagePatch], content: List[str], return_index: bool = False) -> \
        Union[ImagePatch, None]:
    """Returns the patch most likely to contain the content.
    Parameters
    ----------
    list_patches : List[ImagePatch]
    content : List[str]
        the object of interest
    return_index : bool
        if True, returns the index of the patch most likely to contain the object

    Returns
    -------
    int
        Patch most likely to contain the object
    """
    if len(list_patches) == 0:
        return None

    model = 'clip'

    scores = []
    for cont in content:
        if model == 'clip':
            res = list_patches[0].forward(model, [p.cropped_image for p in list_patches], cont, task='compare',
                                          return_scores=True)
        else:
            res = list_patches[0].forward(model, [p.cropped_image for p in list_patches], cont, task='score')
        scores.append(res)
    scores = torch.stack(scores).mean(dim=0)
    scores = scores.argmax().item()  # Argmax over all image patches

    if return_index:
        return scores
    return list_patches[scores]

def compare_relation(obj_1_location,obj_2_location,rel_1,rel_2=None):
    print(rel_1,'rel 1')
    print(obj_1_location,'obj 1')
    print(obj_2_location,'obj2 location')
    if obj_1_location[0] < obj_2_location[0]:
        relation_h = 'to the left'
    else:
        relation_h = 'to the right'
    if obj_1_location[1] < obj_2_location[1]:
        relation_v = 'above'
    else:
        relation_v = 'below'
    

    if rel_2 == None:
        if 'in front' in rel_1:
            # assume in front means larger y and/or higher x 
            if relation_h =='to the left' or relation_v=='below':
                return 'yes'
            else:
                return 'no'
        if 'behind' in rel_1:
            if relation_h =='to the right' or relation_v=='above':
                return 'yes'
            else:
                return 'no'



        if 'left' in rel_1:
            if relation_h == 'to the left':
                return 'yes'
            else:
                return 'no'
        if 'right' in rel_1:
            if relation_h == 'to the right':
                return 'yes'
            else:
                return 'no'
        if any(x in rel_1 for x in ABOVE_WORDS):
            if relation_v == 'above':
                return 'yes'
            else:
                return 'no'

        if any(x in rel_1 for x in BELOW_WORDS):
            if relation_v == 'below':
                return 'yes'
            else:
                return 'no'
        
    else:

        if 'left' in rel_1 or 'left' in rel_2 or 'right' in rel_1 or 'right' in rel_2:
            if relation_h == 'to the left':
                return 'to the left of'
            else:
                return 'to the right of'
        if any(x in rel_1 for x in ABOVE_WORDS) :
            # rel_1 is above 
            # rel_2 is below 
            if relation_v == 'above':
                return rel_1
            else:
                return rel_2 
        if any (x in rel_1 for x in BELOW_WORDS):
            if relation_v == 'below':
                return rel_1
            else:
                return rel_2 
        if any(x in rel_2 for x in ABOVE_WORDS) :
            # rel_1 is above 
            # rel_2 is below 
            if relation_v == 'above':
                return rel_2
            else:
                return rel_1 
        if any (x in rel_2 for x in BELOW_WORDS):
            if relation_v == 'below':
                return rel_2
            else:
                return rel_1 
        if 'front' in rel_1:
            # assume rel_2 is opposite 
            if relation_h =='to the left' or relation_v=='below':
                return rel_1
            else:
                return rel_2
        if 'behind' in rel_1:
            if relation_h =='to the right' or relation_v=='above':
                return rel_1
            else:
                return rel_2


        
    
            


def distance(patch_a: Union[ImagePatch, float], patch_b: Union[ImagePatch, float]) -> float:
    """
    Returns the distance between the edges of two ImagePatches, or between two floats.
    If the patches overlap, it returns a negative distance corresponding to the negative intersection over union.
    """

    if isinstance(patch_a, ImagePatch) and isinstance(patch_b, ImagePatch):
        a_min = np.array([patch_a.left, patch_a.lower])
        a_max = np.array([patch_a.right, patch_a.upper])
        b_min = np.array([patch_b.left, patch_b.lower])
        b_max = np.array([patch_b.right, patch_b.upper])

        u = np.maximum(0, a_min - b_max)
        v = np.maximum(0, b_min - a_max)

        dist = np.sqrt((u ** 2).sum() + (v ** 2).sum())

        if dist == 0:
            box_a = torch.tensor([patch_a.left, patch_a.lower, patch_a.right, patch_a.upper])[None]
            box_b = torch.tensor([patch_b.left, patch_b.lower, patch_b.right, patch_b.upper])[None]
            dist = - box_iou(box_a, box_b).item()

    else:
        dist = abs(patch_a - patch_b)

    return dist


def bool_to_yesno(bool_answer: bool) -> str:
    """Returns a yes/no answer to a question based on the boolean value of bool_answer.
    Parameters
    ----------
    bool_answer : bool
        a boolean value

    Returns
    -------
    str
        a yes/no answer to a question based on the boolean value of bool_answer
    """
    return "yes" if bool_answer else "no"


def llm_query(query, context=None, long_answer=True, queues=None):
    """Answers a text question using GPT-3. The input question is always a formatted string with a variable in it.

    Parameters
    ----------
    query: str
        the text question to ask. Must not contain any reference to 'the image' or 'the photo', etc.
    """
    if long_answer:
        return forward(model_name='gpt3_general', prompt=query, queues=queues)
    else:
        return forward(model_name='gpt3_qa', prompt=[query, context], queues=queues)
def sum_tensor(values:list):
    new_values = []
    for v in values:
        if type(v) != float:
            v = v.item()
        new_values.append(v)
    return sum(new_values)
def avg(values: list):
    new_values = []
    for v in values:
        if type(v) != float:
            v = v.item()
        new_values.append(v)

    return mean(new_values)
def coerce_to_numeric(string, no_string=False):
    """
    This function takes a string as input and returns a numeric value after removing any non-numeric characters.
    If the input string contains a range (e.g. "10-15"), it returns the first value in the range.
    # TODO: Cases like '25to26' return 2526, which is not correct.
    """
    if any(month in string.lower() for month in ['january', 'february', 'march', 'april', 'may', 'june', 'july',
                                                 'august', 'september', 'october', 'november', 'december']):
        try:
            return dateparser.parse(string).timestamp().year
        except:  # Parse Error
            pass

    try:
        # If it is a word number (e.g. 'zero')
        numeric = w2n.word_to_num(string)
        return numeric
    except ValueError:
        pass

    # Remove any non-numeric characters except the decimal point and the negative sign
    string_re = re.sub("[^0-9\.\-]", "", string)

    if string_re.startswith('-'):
        string_re = '&' + string_re[1:]

    # Check if the string includes a range
    if "-" in string_re:
        # Split the string into parts based on the dash character
        parts = string_re.split("-")
        return coerce_to_numeric(parts[0].replace('&', '-'))
    else:
        string_re = string_re.replace('&', '-')

    try:
        # Convert the string to a float or int depending on whether it has a decimal point
        if "." in string_re:
            numeric = float(string_re)
        else:
            numeric = int(string_re)
    except:
        if no_string:
            raise ValueError
        # No numeric values. Return input
        return string
    return numeric
def distance(patch_a: Union[ImagePatch, float], patch_b: Union[ImagePatch, float]) -> float:
    """
    Returns the distance between the edges of two ImagePatches, or between two floats.
    If the patches overlap, it returns a negative distance corresponding to the negative intersection over union.
    """

    if isinstance(patch_a, ImagePatch) and isinstance(patch_b, ImagePatch):
        a_min = np.array([patch_a.left, patch_a.lower])
        a_max = np.array([patch_a.right, patch_a.upper])
        b_min = np.array([patch_b.left, patch_b.lower])
        b_max = np.array([patch_b.right, patch_b.upper])

        u = np.maximum(0, a_min - b_max)
        v = np.maximum(0, b_min - a_max)

        dist = np.sqrt((u ** 2).sum() + (v ** 2).sum())

        if dist == 0:
            box_a = torch.tensor([patch_a.left, patch_a.lower, patch_a.right, patch_a.upper])[None]
            box_b = torch.tensor([patch_b.left, patch_b.lower, patch_b.right, patch_b.upper])[None]
            dist = - box_iou(box_a, box_b).item()

    else:
        dist = abs(patch_a - patch_b)

    return dist