import io
import json
import numpy as np
from PIL import Image
from flask import Flask, jsonify, request
import hnswlib
import torch
import torchvision.transforms as transforms
import timm
from flask import render_template
app = Flask(__name__)

# load hnswlib index and image features
index = hnswlib.Index(space='l2', dim=768)
features = np.load('features.npy', allow_pickle=True)
index.add_items(features)
# load the model
#model = torch.load('ViT-B_16.npz', map_location=torch.device('cpu'))
model = timm.create_model('vit_base_patch16_224', pretrained=True)
model.eval()
# define image preprocessing pipeline
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

@app.route("/")
def home():
    return render_template('index.html')

# define endpoint for searching similar images
@app.route('/search', methods=['POST'])
def search():
    # read image from request
    file = request.files['image']
    image_bytes = io.BytesIO(file.read())
    image = Image.open(image_bytes).convert('RGB')

    # preprocess image and extract features
    input_tensor = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        features_tensor = model(input_tensor).numpy()
        features_vector = features_tensor.reshape(-1)

    # search hnswlib index for similar images
    labels, distances = index.knn_query(features_vector, k=10)

    # format results and return as json
    results = []
    for label, distance in zip(labels[0], distances[0]):
        result = {
            'id': int(label),
            'distance': float(distance),
        }
        results.append(result)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
