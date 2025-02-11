import torch

from .aro_dataset import VG_Relation, VG_Attribution, COCO_Order, Flickr30k_Order
from .retrieval import COCO_Retrieval, Flickr30k_Retrieval


def get_dataset(dataset_name, image_preprocess=None, text_perturb_fn=None, image_perturb_fn=None, download=False, *args, **kwargs):
    """
    Helper function that returns a dataset object with an evaluation function. 
    dataset_name: Name of the dataset.
    image_preprocess: Preprocessing function for images.
    text_perturb_fn: A function that takes in a string and returns a string. This is for perturbation experiments.
    image_perturb_fn: A function that takes in a PIL image and returns a PIL image. This is for perturbation experiments.
    download: Whether to allow downloading images if they are not found.
    """
    if dataset_name == "VG_Relation": 
        from .aro_datasets import get_visual_genome_relation
        return get_visual_genome_relation(image_preprocess=image_preprocess, text_perturb_fn=text_perturb_fn, image_perturb_fn=image_perturb_fn, download=download, *args, **kwargs)
    elif dataset_name == "VG_Attribution":
        from .aro_datasets import get_visual_genome_attribution
        return get_visual_genome_attribution(image_preprocess=image_preprocess, text_perturb_fn=text_perturb_fn, image_perturb_fn=image_perturb_fn, download=download, *args, **kwargs)
    elif dataset_name == "COCO_Order":
        from .aro_datasets import get_coco_order
        return get_coco_order(image_preprocess=image_preprocess, text_perturb_fn=text_perturb_fn, image_perturb_fn=image_perturb_fn, download=download, *args, **kwargs)
    elif dataset_name == "Flickr30k_Order":
        from .aro_datasets import get_flickr30k_order
        return get_flickr30k_order(image_preprocess=image_preprocess, text_perturb_fn=text_perturb_fn, image_perturb_fn=image_perturb_fn, download=download, *args, **kwargs)
    elif dataset_name == "COCO_Retrieval":
        from .retrieval import get_coco_retrieval
        return get_coco_retrieval(image_preprocess=image_preprocess, text_perturb_fn=text_perturb_fn, image_perturb_fn=image_perturb_fn, download=download, *args, **kwargs)
    elif dataset_name == "Flickr30k_Retrieval":
        from .retrieval import get_flickr30k_retrieval
        return get_flickr30k_retrieval(image_preprocess=image_preprocess, text_perturb_fn=text_perturb_fn, image_perturb_fn=image_perturb_fn, download=download, *args, **kwargs)
    else:
        raise ValueError(f"Unknown dataset {dataset_name}")

def general_postprocessing(prediction):
    try:
        if type(prediction).__name__ == 'ImagePatch':
            prediction = prediction.classify_object()

        if isinstance(prediction, list):
            prediction = prediction[0] if len(prediction) > 0 else "no"

        if isinstance(prediction, torch.Tensor):
            prediction = prediction.item()
        if prediction is None:
            prediction = "no"
        if isinstance(prediction, bool):
            if prediction:
                prediction = "yes"
            else:
                prediction = "no"
        elif isinstance(prediction, int):
            prediction = str(prediction)
            print("No answer is a number, so this will be wrong")
    except:
        prediction = str(prediction)

    prediction = str(prediction)

    prediction = prediction.replace('\n', ' ')
    prediction = prediction.replace('\t', ' ')
    prediction = prediction.strip()
    prediction = prediction.lower()

    if prediction == 'true':
        prediction = 'yes'
    elif prediction == 'false':
        prediction = 'no'
    return prediction


def accuracy(prediction, ground_truth, *args):
    """
    Args:
        prediction (list): List of predicted answers.
        ground_truth (list): List of ground truth answers.
    Returns:
        score (float): Score of the prediction.
    """
    if len(prediction) == 0:  # if no prediction, return 0
        return 0
    assert len(prediction) == len(ground_truth)
    pred_gt_filtered = [(pred, gt) for pred, gt in zip(prediction, ground_truth) if gt != '']
    score = 0
    for p, g in pred_gt_filtered:
        if general_postprocessing(p) == g:
            score += 1
    return score / len(pred_gt_filtered)
