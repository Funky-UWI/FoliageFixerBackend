import torch
import torch.nn as nn
import torchvision

class ClassificationModel(nn.Module):
    def __init__(self, num_classes=8):
        super().__init__()
        # Define your classification model here
        self.classification = torchvision.models.resnet18(pretrained=True)
        # Replace the last layer with a new layer that has num_classes outputs
        num_features = self.classification.fc.in_features
        self.classification.fc = nn.Linear(num_features, num_classes)
        self.label_dict = train_set.class_to_idx
    
    def forward(self, x):
        # Forward pass through the classification model
        x = self.classification(x)
        return x