import os
import cv2
import numpy as np

DATA_DIR = "./data"
CLASSES = ["Demo_Tomato_Healthy", "Demo_Tomato_Early_Blight"]

def create_demo_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    print("Generating demo images...")
    
    for class_name in CLASSES:
        class_dir = os.path.join(DATA_DIR, class_name)
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)
            
        # Create 5 dummy images per class
        for i in range(5):
             # Just random noise images, enough to make the training loop run
            img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
            save_path = os.path.join(class_dir, f"img_{i}.jpg")
            cv2.imwrite(save_path, img)
            
    print(f"✅ Created demo data in {DATA_DIR} for classes: {CLASSES}")
    print("You can now run 'python train_model.py'!")

if __name__ == "__main__":
    create_demo_data()
