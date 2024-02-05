import torch
from torch import nn
import torchvision
from torchvision import models, transforms
from PIL import Image
import numpy as np

# Device agnostic code
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Loading Vision Transformer model
model = models.vit_b_16(pretrained=True)

# Modifying  the last layer
model.heads = nn.Linear(in_features=768,
                        out_features=101)

# Loading saved weight
saved_state_dict = torch.load('static/model/vit_model.pth',
                              map_location=torch.device('cpu'))

# Loading the weight into model
model.load_state_dict(saved_state_dict)

# Define data transformations
transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


# Prediction 
def prediction(image_path):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)
    output = model(image)
    output = output.detach().numpy() 
    index = np.argmax(output)
    return index

