import torch 
from typing import List
from torchvision.ops import box_iou
from typing import Union, List
import cv2
from PIL import Image
from transformers import OwlViTProcessor, OwlViTForObjectDetection
from torchvision import transforms
from transformers import AutoProcessor, BlipForQuestionAnswering
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch.nn.functional as F
from transformers import AutoTokenizer, BertModel
from X_VLM_master.models import model_retrieval 
import numpy as np
PRETRAINED_FILE_PATH= '/home/michal5/pretrained_models/xvlm_old/checkpoint_9.pth'
XVLM_PREFIX = '/home/michal5/LAVIS/X_VLM_master/'
DEVICE = 'cuda'


def bool_to_yesno(bool_answer:bool)-> str:
   return 'yes' if bool_answer else 'no'

class ImagePatch:
    """A Python class containing a crop of an image centered around a particular object, as well as relevant information.
    Attributes
    ----------
    cropped_image : array_like
        An array-like of the cropped image taken from the original image.
    left : int
        An int describing the position of the left border of the crop’s bounding box in the original image.
    lower : int
        An int describing the position of the bottom border of the crop’s bounding box in the original image.
    right : int
        An int describing the position of the right border of the crop’s bounding box in the original image.
    upper : int
        An int describing the position of the top border of the crop’s bounding box in the original image.
    Methods
    -------
    find(object_name: str)->List[ImagePatch]
        Returns a list of new ImagePatch objects containing crops of the image centered around any objects found in the image matching the object_name.
    exists(object_name: str)->bool
        Returns True if the object specified by object_name is found in the image, and False otherwise.
    verify_property(property: str)->bool
        Returns True if the property is met, and False otherwise.
    best_text_match(option_list: List[str], prefix: str)->str
        Returns the string that best matches the image.
    simple_query(question: str=None)->str
        Returns the answer to a basic question asked about the image. If no question is provided, returns the answer to "What is this?".
    compute_depth()->float
        Returns the median depth of the image crop.
    crop(left: int, lower: int, right: int, upper: int)->ImagePatch
        Returns a new ImagePatch object containing a crop of the image at the given coordinates.
    """
    def __init__(self, image, left: int=None, lower: int=None, right: int=None, upper: int=None): 
        """
        Initializes an ImagePatch object by cropping the image at the given coordinates and stores the coordinates as attributes. If no coordinates are provided, the image is left unmodified, and the coordinates are set to the dimension of the image.
        -----
        image: array_like
            An array-like of the original image 
        left: int
            An int describing the position of the left border of the crop's bounding box in the original image.
        lower: int 
            An int describing the position of the bottom border of the crop's bounding box in the original image.
        right: int 
            An int describing the position of the right border of the crop's bounding box in the original image.
        upper: int
            An int describing the position of the top border of the crop's bounding box in the original image.

        """
        if left is None and right is None and upper is None and lower is None:
            self.cropped_image = image
            self.left = 0 
            self.lower = 0
            self.right = image.shape[2] #width 
            self.upper = image.shape[1] #height 
            self.height = image.shape[1]
            self.width = image.shape[2]
        else:

            self.cropped_image = image[:,lower:upper,left:right]
            self.left = left 
            self.upper = upper 
            self.right = right 
            self.lower = lower 
            self.width = self.cropped_image.shape[2]
            self.height = self.cropped_image.shape[1]

            self.horizontal_center = (self.left+self.right)/2
            self.vertical_center = (self.lower+self.upper)/2
    def find(self, object_name: str):
        """
        Returns a list of ImagePatch objects matching object_name contained in the crop if they are found. Otherwise retruns an empty list.
        Parameters
        ---------
        object_name: str
            the name of the object to be found
        Returns 
        ---------
        List[ImagePatch]
            a list of ImagePatch objects matching object_name contained in the crop
        Examples
        --------
        >>> # return the children
        >>> def execute_command(image) -> List[ImagePatch]:
        >>>  image_patch = ImagePatch(image)
        >>>  children = image_patch.find("child")
        >>>  return children 
        """
        all_image_patches = []
        find_processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
        find_model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32")
        find_model = find_model.to(DEVICE)
        text_prompt = [['a photo of a ' + object_name]]
        inputs = find_processor(text=text_prompt,images=self.cropped_image,return_tensors="pt").to(DEVICE)
        with torch.no_grad():
            outputs = find_model(**inputs)
        target_sizes = torch.Tensor([[self.right,self.upper]]).to(DEVICE)
        results = find_processor.post_process(outputs=outputs,target_sizes=target_sizes)
        i = 0
        text = text_prompt[i]
        boxes, scores,labels = results[i]["boxes"],results[i]["scores"],results[i]["labels"]
        threshold_boxes = []
        for box,score,label in zip(boxes,scores,labels):
            box = [round(i,2) for i in box.tolist()]
            if score >= 0.01:
                threshold_boxes.append(box)
        for b in threshold_boxes:
            # print(self.cropped_image.shape)
            #print(int(b[0]),int(b[1]),int(b[2]),int(b[3]))
            # print(self.cropped_image[:,int(b[0]):int(b[1]),int(b[2]):int(b[3])])
            new_patch = ImagePatch(image=self.cropped_image,left=int(b[0]),upper=int(self.height - b[1]),right=int(b[2]),lower=int(self.height-b[3]))
            #print(new_patch.cropped_image)
            all_image_patches.append(new_patch)
        return all_image_patches
    def exists(self,object_name: str) -> bool:
        """
        Returns True if the object specified by the object_name is found in the image, and False otherwise.
        Parameters
        ----------
        object_name: str
            A string describing the name of the object to be found in this image
        Examples
        --------
        >>> #Are there both cake and gummy bears in the photo?
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     is_cake = image_patch.exists("cake")
        >>>     is_gummy_bear = image_patch.exists("gummy bear")
        >>>     return bool_to_yesno(is_cake and is_gummy_bear)
        """
        return len(self.find(object_name))>0
    def verify_property(self,object_name: str, property: str)-> bool:
        """
        Returns True if the object posses the property and False otherwise. Differs from 'exists' in that it presupposes the
        existence of the object specified by object_name, instead checking whether the object posses the property.
        Parameters
        ----------
        object_name: str
            A string describing the name of the object to be found in the image
        property: str
            A string describing the property to be checked
        Examples 
        --------
        >>> #Do the letters have blue color?
        >>> def execute_command(image) -> str:
        >>>     image_patch = ImagePatch(image)
        >>>     letters_patches = image_patch.find("letters")
        >>>     #Question assumes only one letter patch
        >>>     if len(letters_patches) == 0:
        >>>         #If no letters are found, query the image directly
        >>>         return image_patch.simple_query("Do the letters have blue color?")
        >>>     return bool_to_yesno(letters_patches[0].verify_property("letters","blue"))
        """
        
        xvlm_checkpoint = torch.load(PRETRAINED_FILE_PATH)
        xvlm_config = xvlm_checkpoint['config']
        xvlm_config['vision_config'] = XVLM_PREFIX + xvlm_config['vision_config']
        xvlm_config['text_config'] = XVLM_PREFIX + xvlm_config['text_config']
        retrieval_model = model_retrieval.XVLM(config=xvlm_config)
        retrieval_model.load_pretrained(PRETRAINED_FILE_PATH,xvlm_config)
        retrieval_model = retrieval_model.to(DEVICE)
        tokenizer =  AutoTokenizer.from_pretrained("bert-base-uncased")
        # text input is object name and property+object name
        text_inputs = [object_name, property+' '+object_name]
        all_text_embeds = []
        retrieval_model.eval()
        for text in text_inputs:
            with torch.no_grad():
                tokenized = tokenizer(text,return_tensors='pt')
                tokenized = tokenized.to(DEVICE)
                text_encoded = retrieval_model.text_encoder(tokenized.input_ids,attention_mask=tokenized.attention_mask,mode='text')
                text_feat = text_encoded.last_hidden_state
                text_embed = F.normalize(retrieval_model.text_proj(text_feat[:, 0, :]))
                all_text_embeds.append(text_embed.cpu())
        all_text_embeds = torch.cat(all_text_embeds)
        normalize = transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        test_transform = transforms.Compose([
            transforms.Resize((xvlm_config['image_res'], xvlm_config['image_res']), interpolation=Image.BICUBIC),
            transforms.ToTensor(),
            normalize,
        ])
        #print(self.cropped_image)
        print(self.cropped_image.shape)
        pil_image = np.transpose(self.cropped_image, (1,2,0))
        pil_image = Image.fromarray(pil_image)
        transform_img = test_transform(pil_image)
        with torch.no_grad():
            transform_img = torch.unsqueeze(transform_img,0)
            transform_img = transform_img.to(DEVICE)
            encoded_img = retrieval_model.vision_encoder(transform_img)
            image_embed = retrieval_model.vision_proj(encoded_img[:, 0, :])
            image_embed = F.normalize(image_embed, dim=-1)
        
        sims_matrix = (image_embed.cpu() @ all_text_embeds.t())/retrieval_model.temp.cpu()
        max_idx = torch.argmax(sims_matrix).item()
        return bool_to_yesno(max_idx==1)
    def simple_query(self, question: str = None) -> str:
        """
        Returns the answer to a basic question asked about the image. If no question is provided, returns the answer to 'What is this?'
        Parameters
        ----------
        question: str
            A string describing the question to be asked
        Examples
        --------
        >>> # What kind of animal is not eating?
        >>> def execute_command(image) -> str:
        >>>      image_patch = ImagePatch(image)
        >>>      animal_patches = image_patch.find("animal")
        >>>      for animal_patch in animal_patches:
        >>>          if not animal_patch.verify_property("animal","eating"):
        >>>              return animal_patch.simple_query("What kind of animal is eating?")#crop would include eating so keep it in query
        >>>      #If not animal is eating, query the image directly
        >>>      return image_patch.simple_query("What kind of animal is not eating?")
        
        >>> # What is in front of the horse?
        >>> # contains a relation (around, next to, on, near, on top of, in front of, behind, etc) so ask directly
        >>> return impage_patch.simple_query("What is in front of the horse?")
        """
        blip_processor =  Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xl")
        blip_model =  Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-flan-t5-xl",torch_dtype=torch.float16)
        blip_model.eval()
        blip_model = blip_model.to(DEVICE)
        question_prompt = 'Question: '+question+' Answer:'
        inputs = blip_processor(images=self.cropped_image,text=question_prompt,return_tensors="pt").to(DEVICE,torch.float16)

        generated_output = blip_model.generate(**inputs)
        #print(blip_processor.batch_decode(generated_output,skip_special_tokens=True))
        answer = blip_processor.batch_decode(generated_output,skip_special_tokens=True)[0].strip()
        return answer 
    def best_text_match(self, option_list: List[str]) -> str:
        """
        Returns the string that best matches the iamge.
        Parameters
        ----------
        option_list: str
            A list with the names of the different options
        prefix: str
            A string with the prefixes to append to the options
        Examples
        --------
        >>> # Is the cap gold or white?
        >>> def execute_command(image)-> str:
        >>>      image_patch = ImagePatch(image)
        >>>      cap_patches = image_patch.find('cap')
        >>>      # Question assumes one cap patch
        >>>      If len(cap_patches) == 0:
        >>>          #If no cap is found, query the image directly
                        return image_patch.simple_query("Is the cap gold or white?"
        >>>      return cap_patches[0].best_text_match(["gold","white"]) 
        """
        xvlm_checkpoint = torch.load(PRETRAINED_FILE_PATH)
        xvlm_config = xvlm_checkpoint['config']
        xvlm_config['vision_config'] = XVLM_PREFIX + xvlm_config['vision_config']
        xvlm_config['text_config'] = XVLM_PREFIX + xvlm_config['text_config']
        retrieval_model = model_retrieval.XVLM(config=xvlm_config)
        retrieval_model.load_pretrained(PRETRAINED_FILE_PATH,xvlm_config)
        retrieval_model = retrieval_model.to(DEVICE)
        tokenizer =  AutoTokenizer.from_pretrained("bert-base-uncased")
        # text input is object name and property+object name
        text_inputs = option_list
        all_text_embeds = []
        retrieval_model.eval()
        for text in text_inputs:
                with torch.no_grad():
                    tokenized = tokenizer(text,return_tensors='pt')
                    tokenized = tokenized.to(DEVICE)
                    text_encoded = retrieval_model.text_encoder(tokenized.input_ids,attention_mask=tokenized.attention_mask,mode='text')
                    text_feat = text_encoded.last_hidden_state
                    text_embed = F.normalize(retrieval_model.text_proj(text_feat[:, 0, :]))
                    all_text_embeds.append(text_embed.cpu())
        all_text_embeds = torch.cat(all_text_embeds)
        normalize = transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        test_transform = transforms.Compose([
            transforms.Resize((xvlm_config['image_res'], xvlm_config['image_res']), interpolation=Image.BICUBIC),
            transforms.ToTensor(),
            normalize,])
        transform_img = test_transform(self.cropped_image)
        with torch.no_grad():
                    transform_img = torch.unsqueeze(transform_img,0)
                    transform_img = transform_img.to(DEVICE)
                    encoded_img = retrieval_model.vision_encoder(transform_img)
                    image_embed = retrieval_model.vision_proj(encoded_img[:, 0, :])
                    image_embed = F.normalize(image_embed, dim=-1)
        sims_matrix = (image_embed.cpu() @ all_text_embeds.t())/retrieval_model.temp 
        max_idx = torch.argmax(sims_matrix).item()
        return option_list[max_idx.item()]
    def compute_depth(self):
         """
         Returns the median depth of the image crop
         Parameters
         ----------
         Returns 
         ----------
         float
            the median depth of the image crop
         Examples
         --------
         >>>    # the person furthest away
         >>>    def execute_command(image)-> ImagePatch:
         >>>        image_patch = ImagePatch(image)
         >>>        person_patches = image_patch.find("person")
         >>>        person_patches.sort(key=lambda person: person.compute_depth())
         >>>        return person_patches[-1]
         """
         midas = torch.hub.load("intel-isl/MiDaS", 'DPT_Large')
         midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
         transform = midas_transforms.dpt_transform
         #print(self.cropped_image.shape)
         image = torch.tensor(self.cropped_image).permute(1, 2, 0)
         image = image.numpy()
         image = transform(image)
         midas = midas.to('cuda')
         image = image.to('cuda')
         with torch.no_grad():
            prediction = midas(image)

            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=self.cropped_image.shape[:2],mode="bicubic",align_corners=False,).squeeze()
         output = 1/prediction.cpu()
         depth_map = output[self.cropped_image.shape[1]-self.upper:self.cropped_image.shape[1]-self.lower,
                              self.left:self.right]
         return depth_map.median()
    def crop(self, left: int, lower:int, right: int, upper: int):
         """
         Returns a new ImagePatch cropped from the current ImagePatch.
         Parameters
         ---------
         left: int
            The leftmost pixel of the cropped image
         lower: int
            The lowest pixel of the cropped image
         right: int 
            The rightmost pixel of the cropped image.
         upper: int
            The uppermost pixel of the cropped image.
         """
         return ImagePatch(self.cropped_image,left,lower,right,upper)
    def overlaps_with(self,left,lower,right,upper):
         """
         Returns True if a crop with the given coordinates overlaps with this one, else False
         Parameters
         ---------
         left: int
            the left border of the crop to be checked
         lower: int
            the lower border of the crop to be checked
         right: int 
            the right border of the crop to be checked
         upper: int
            the upper border of the crop to be checked
         Returns 
         -------
         bool
            True if a crop with the given coordinates overlaps with this one, else False
         Examples
         ---------
         >>> #black cup on top of the table
         >>> def execute_command(image) -> ImagePatch:
         >>>    image_patch = ImagePatch(image)
         >>>    table_patches = image_patch.find("table")
         >>>    if len(table_patches) == 0:
         >>>        table_patches =[image_patch] # If no table found, assume the whole image is a table
         >>>    cup_patches = image_patch.find("black cup")
         >>>    for cup in cup_patches:
         >>>        if cup.vertical_center > table_patch.vertical_center
         >>>            return cup
         >>>    return cup_patches[0] # If no cup found on top of the table, return the first cup found
         """
         return self.left <= self.right >= left and self.lower <= upper and self.upper>= lower 
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








