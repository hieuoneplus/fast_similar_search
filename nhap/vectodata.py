import os
import torch
import torchvision.transforms as transforms
import timm
import numpy
from PIL import Image



def extract_features(image_path, model):
    """Extract features from a single image using a pre-trained ViT model"""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    image = Image.open(image_path)
    image = transform(image)
    image = image.unsqueeze(0)
    features = model.forward_features(image)
    return features.squeeze().detach().numpy()


def extract_dataset_features(dataset_path, model):
    """Extract features from all images in a dataset using a pre-trained ViT model"""
    features = {}
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                image_path = os.path.join(root, file)
                features[image_path] = extract_features(image_path, model)
    return features


if __name__ == '__main__':
    # Load pre-trained ViT model
    model = timm.create_model('vit_base_patch16_224', pretrained=True)
    model.eval()

    # Extract features from a dataset of images
    dataset_path = 'C:/Users/nshd1/OneDrive/Documents/code/fss/data'
    features = extract_dataset_features(dataset_path, model)

    # Save features to a numpy file
    numpy_file = 'features.npy'
    numpy.save(numpy_file, features)
