import os
import torch
import torchvision.transforms as transforms
import numpy as np
import hnswlib
from PIL import Image
from timm import create_model

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
    features = model(image)
    return features.detach().numpy()

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
    model = create_model('vit_base_patch16_224', pretrained=True)
    model.head = torch.nn.Identity()
    model.eval()

    # Extract features from a dataset of images
    dataset_path = 'C:/Users/nshd1/OneDrive/Documents/code/fast_similar_search/static/image'
    features = extract_dataset_features(dataset_path, model)

    # Convert features to 2D array
    num_images = len(features)
    dim = next(iter(features.values())).shape[1]
    features_array = np.zeros((num_images, dim), dtype=np.float32)
    for i, feature in enumerate(features.values()):
        features_array[i, :] = feature

    # Create index
    index = hnswlib.Index(space='l2', dim=dim)
    index.init_index(max_elements=num_images, ef_construction=600, M=64)

    # Add items to index
    index.add_items(features_array)

    # Save index
    index.save_index('index.bin')
    print(num_images)














