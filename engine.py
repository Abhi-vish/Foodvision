import torch
from torch import nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
from transformers import ViTFeatureExtractor, ViTForImageClassification

# Device agnostic code
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load pre-trained ViT model
model_name = "google/vit-base-patch16-224-in21k"
feature_extractor = ViTFeatureExtractor(model_name)
model = ViTForImageClassification.from_pretrained(model_name)

# Modifying the classifier layer as our need
num_classes = 101
model.classifier = torch.nn.Linear(in_features=model.config.hidden_size,
                                   out_features=num_classes)

# Checkpoint
checkpoint = torch.load("static/model/vit_fine_tuned_model.pth",
                        map_location=torch.device('cpu'))
model.load_state_dict(checkpoint)

# Prepare the dataset
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Prediction
def prediction(image_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    with torch.no_grad():
        image = Image.open(image_path)
        input_tensor = transform(image).unsqueeze(0).to(device)

        output = model(input_tensor).logits
        _, index = torch.max(output, 1)

    return index.item()