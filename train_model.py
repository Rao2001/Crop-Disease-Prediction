import json
import os
import tensorflow as tf
from src.data_loader import load_data
from src.model_builder import build_transfer_model
from src.trainer import train_job

# Configuration
DATA_DIR = "./data"
MODEL_DIR = "./models"
IMG_SIZE = 224
BATCH_SIZE = 8
EPOCHS = 20

def main():
    print(f"Starting Training Pipeline...")
    print(f"Looking for data in: {os.path.abspath(DATA_DIR)}")
    
    # 1. Load Data
    try:
        train_ds, val_ds, class_names = load_data(DATA_DIR, IMG_SIZE, BATCH_SIZE)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 TIP: Create a folder inside 'data/' for each disease class and put images in them.")
        return

    num_classes = len(class_names)
    print(f"Found {num_classes} classes: {class_names}")
    
    # 2. Save Class Indices (CRITICAL for App)
    # The app needs to know that Index 0 = "Apple_Scab", Index 1 = "Corn_Rust", etc.
    class_indices = {i: name for i, name in enumerate(class_names)}
    
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        
    indices_path = os.path.join(MODEL_DIR, "class_indices.json")
    with open(indices_path, "w") as f:
        json.dump(class_indices, f, indent=4)
    print(f"Class mappings saved to {indices_path}")
    
    # 3. Build Model
    model = build_transfer_model(num_classes, IMG_SIZE)
    model.summary()
    
    # 4. Train
    print("\nTraining MobileNetV2 Transfer Model...")
    history = train_job(model, train_ds, val_ds, epochs=EPOCHS, model_save_path=os.path.join(MODEL_DIR, "crop_disease_model.h5"))
    
    print("\nTraining Complete! Model saved to models/crop_disease_model.h5")

if __name__ == "__main__":
    main()
