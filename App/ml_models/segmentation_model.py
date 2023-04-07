import torch
import torch.nn as nn
import torchvision
import io
import PIL

class SegmentationModel(nn.Module):
    def __init__(self, seg_path='App/ml_models/mobilenetv2.3'):
        super().__init__()
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
            print(torch.cuda.get_device_name(device))
        else:
            self.device = None
            print('GPU is not available')
        # Define your segmentation model here
        # self.segmentation = models.segmentation.__dict__["fcn_resnet50"](pretrained=True)
        self.segmentation = torch.load(seg_path, map_location=torch.device('cpu'))
        # Freeze the segmentation layers
        for param in self.segmentation.parameters():
            param.requires_grad = False

    def forward(self, x):
        device = self.device
        # Forward pass through the segmentation model
        # x = x/255.0
        # resize
        x = torchvision.transforms.Resize(size=(512,512))(x)
        if x.shape[1] == 4:
          # if batch_size is 1
          if x.shape[0] == 1:
            img = x.squeeze(0)
            # transpose to shape: 512, 512, 4
            img = np.transpose(img, (1,2,0))
            pil_image = PIL.Image.fromarray(img.numpy(), 'RGBA')
            rgb_image = pil_image.convert('RGB')
            rgb_array = np.asarray(rgb_image, dtype=np.float32)
            x = torch.from_numpy(np.transpose(rgb_array, (2,1,0)))
            x = x.unsqueeze(0)
        x = x.to(device=device)
        # segment image first
        outputs = self.segmentation(x)
        # Apply softmax activation function to the output
        probs = torch.softmax(outputs, dim=1)
        # Get the predicted labels
        _, labels = torch.max(probs, dim=1)

        disease_mask = (labels == 2).float()
        disease_mask = torch.unsqueeze(disease_mask, 1)
        healthy_mask = (labels == 1).float()
        healthy_mask = torch.unsqueeze(healthy_mask, 1)
        leaf_mask = disease_mask + healthy_mask

        disease = x * disease_mask
        leaf = x * leaf_mask
        return (leaf, disease)