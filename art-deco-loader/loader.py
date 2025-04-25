import base64
import numpy as np
import pandas as pd
import requests
import torch

from transformers import CLIPProcessor, CLIPModel
from PIL import Image

# sample_count = 5000

# Load the processor and model
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

# Load the data and pull out some samples
data = pd.read_csv('artwork-data.csv')
# data = data.head(sample_count)
# data = data.sample(sample_count)

# loop through the selected rows
for index, row in data.iterrows():
    # Extract the values from the row
    title = row['title']
    author = row['author']
    image_url = row['image_url']

    # Preprocess image
    try:
      image = Image.open(requests.get(image_url, stream=True).raw)
      inputs = processor(images=image, return_tensors="pt")
    except Exception as e:
      print(f"Error processing image {image_url}: {e}")
      continue

    # Extract image embedding (batch_size x 512)
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    # Convert to numpy array and normalize
    embedding = image_features[0].numpy()
    embedding /= np.linalg.norm(embedding)

    # Convert to base64
    embedding_bytes = embedding.astype(np.float32).tobytes()
    embedding_b64 = base64.b64encode(embedding_bytes).decode('utf-8')

    # Send the embedding to the server using the request body and forms
    response = requests.post(
        'http://localhost:8000/items',
        data={
            'title': title,
            'author': author,
            "image_url": image_url,
            'embedding': embedding_b64,
        },
    )

    print(response.status_code, response.json()['image_url'])

