import tensorflow as tf
import numpy as np
from PIL import Image

def load_model(model_path):
    """
    Loads the trained Keras model.
    """
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except OSError:
        return None

import json
import os

def load_class_indices():
    """
    Loads the dynamic class mappings from the JSON file created during training.
    """
    path = './models/class_indices.json'
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        # JSON keys are always strings, convert back to int if needed, 
        # but here we just need the values in order usually.
        # Actually our map is "0": "Apple", so we can just use it directly.
        return json.load(f)

def predict_image(image, model):
    """
    Preprocesses the image and runs inference using the loaded model.
    """
    if model is None:
        return None, 0.0

    # Ensure image is RGB (removes alpha channel if present)
    image = image.convert('RGB')

    # Resize image to match model input (MobileNetV2 uses 224x224 usually, but we kept variable in builder)
    # NOTE: Check if model builder used 224 or 256. 
    # Standard MobileNet is 224. The script uses 224.
    image = image.resize((224, 224))
    
    # Convert to array
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    
    # MobileNetV2 expects inputs [-1, 1] or [0, 1] depending on specific preprocess function.
    # tf.keras.applications.mobilenet_v2.preprocess_input expects [-1, 1].
    # But our builder used `include_top=False` and didn't bake in preprocessing layer explicitly 
    # in the sequential block usually, BUT MobileNetV2 has internal scaling if using the application object?
    # Actually, standard practice: divide by 127.5 and subtract 1.
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    
    # Create a batch
    img_array = tf.expand_dims(img_array, 0)
    
    # Run prediction
    predictions = model.predict(img_array)
    
    # Get Dynamic Classes
    full_indices = load_class_indices()
    
    if full_indices:
        # JSON loads keys as strings "0", "1"...
        predicted_index = np.argmax(predictions[0])
        predicted_class = full_indices.get(str(predicted_index), "Unknown Class")
    else:
        # Fallback if JSON missing (should n't happen in proper flow)
        predicted_class = f"Class {np.argmax(predictions[0])}"

    confidence = round(100 * (np.max(predictions[0])), 2)
    
    return predicted_class, confidence
