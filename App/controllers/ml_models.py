from App.ml_models import ( SegmentationModel, ClassificationModel )

import torch
import torch.nn as nn
import torchvision
import io
import PIL

segmentation_model = SegmentationModel()

# classification_model = ClassificationModel()

'''
load seg model
'''
def get_segmentation_model():
    return segmentation_model

'''
load class model
'''
# def get_classification_model():
#     return classification_model

'''
/classify route receives uploaded image as a FileStorage object. 
This code converts it to a tensor so it can be sent to the model.
'''
def FileStorage_to_Tensor(file_storage_object):
    image_binary = file_storage_object.read()
    pil_image = PIL.Image.open(io.BytesIO(image_binary))
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        # transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    tensor_image = transform(pil_image)
    return tensor_image
    
'''
Calculate severity.
'''
def compute_severity(leaf, disease):
    # Check the shape of the tensor (should be in the format C x H x W)
    C, H, W = leaf.shape
    # Flatten the tensor to a 2D matrix
    image_flat = leaf.view(C, H * W)
    # Count the number of non-black pixels (i.e. pixels with at least one non-zero channel)
    leaf_pixels = torch.sum(torch.any(image_flat != 0, dim=0))
    # Print the number of non-black pixels
    print("Leaf Non Black Pixels:", leaf_pixels.item())

     # Check the shape of the tensor (should be in the format C x H x W)
    C, H, W = disease.shape
    # Flatten the tensor to a 2D matrix
    image_flat = disease.view(C, H * W)
    # Count the number of non-black pixels (i.e. pixels with at least one non-zero channel)
    disease_pixels = torch.sum(torch.any(image_flat != 0, dim=0))
    # Print the number of non-black pixels
    print("Disease Non Black Pixels:", disease_pixels.item())

    severity = disease_pixels / (leaf_pixels + disease_pixels)

    return severity.item() * 100