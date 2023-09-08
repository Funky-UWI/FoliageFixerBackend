from App.ml_models import ( SegmentationModel, ClassificationModel )

import torch
import torch.nn as nn
import torchvision
import io
import PIL

import requests

segmentation_model = SegmentationModel()

classification_model = ClassificationModel()
# weights_path = 'App/ml_models/classification-v3_stateDict'
# classification_model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
# classification_model.train(mode=False)

label_dict = {
    'Bacterial Spot': 0, 
    'Early Blight': 1, 
    'Healthy': 2, 
    'Late Blight': 3,
    'Leaf Mold': 4, 
    'Septoria Leaf Spot': 5, 
    'Tomato Mosaic Virus': 6, 
    'Yellow Leaf Curl Virus': 7
    }



'''
load seg model
'''
def get_segmentation_model():
    return segmentation_model

'''
load class model
'''
def get_classification_model():
    # return torch.load('App/ml_models/classification-v1')
    return classification_model

'''
get predicted classification
'''
def get_classification(outputs):
    outputs = torch.from_numpy(outputs)
    probabilities = torch.softmax(outputs, dim=1)
    # this id may not be related to database ids
    predicted_class_id = torch.argmax(probabilities, dim=1)
    predicted_class = get_class_from_id(predicted_class_id.cpu().numpy()[0])
    return predicted_class

def get_class_from_id(id):
  label = list(label_dict.keys())[list(label_dict.values()).index(id)]
  return label

'''
/classify route receives uploaded image as a FileStorage object. 
This code converts it to a tensor so it can be sent to the model.
'''
def FileStorage_to_Tensor(file_storage_object):
    # image_binary = file_storage_object.read()
    image_binary = file_storage_object
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
    print(type(leaf))
    # Flatten the tensor to a 2D matrix
    image_flat = leaf.view(C, H * W)
    print(image_flat)
    # Count the number of non-black pixels (i.e. pixels with at least one non-zero channel)
    leaf_pixels = torch.sum(torch.any(image_flat != 0, dim=0))
    print(leaf_pixels)
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

    severity = disease_pixels.item() / (leaf_pixels.item() + disease_pixels.item())

    return severity * 100


def request_classification_from_azure(image_bytes, url='https://foliagefixermodel.azurewebsites.net/api/foliagefixermodel'):
    form_data = {
        "image": image_bytes
    }
    response = requests.post(url, files=form_data)

    return response
