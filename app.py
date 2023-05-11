from flask import Flask, render_template, request
import hnswlib
import torch
import torchvision.transforms as transforms
from PIL import Image
import timm
from indexbin import extract_features
import os

folder_path = 'C:/Users/nshd1/OneDrive/Documents/code/fast_similar_search/static/image'

file_list = os.listdir(folder_path)

# Load the hnswlib index
index = hnswlib.Index(space='l2', dim=512)
index.load_index('index.bin')

# Load the PyTorch model
model = timm.create_model('vit_base_patch16_224', pretrained=True)
model.head = torch.nn.Identity()
model.eval()

# Define the Flask app
app = Flask(__name__)


# Define the route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Define the route for the search page
@app.route('/search', methods=['POST'])
def search():
    # Get the uploaded image
    image = request.files['image']

    # Extract features from the uploaded image
    features = extract_features(image, model)

    # Search for similar images using hnswlib
    labels, distances = index.knn_query(features, k=10)

    # Return the results
    return render_template('search.html', labels=labels, distances=distances, list=file_list)
    
# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
