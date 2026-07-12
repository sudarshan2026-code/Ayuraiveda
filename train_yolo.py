"""
YOLOv8 prakriti Classifier Training Script
Downloads yolov8n-cls.pt (nano classification model) and trains it on yolo_dataset
"""

import os
import shutil
from ultralytics import YOLO

def main():
    print("=" * 60)
    print("Training YOLOv8 Prakriti Classification Model")
    print("=" * 60)
    
    # 1. Initialize YOLO classification model
    print("Initializing yolov8n-cls.pt...")
    model = YOLO('yolov8n-cls.pt')
    
    # 2. Train model
    # We use 10 epochs and image size 128 for very fast training (since it's a light classifier)
    print("Starting training on dataset...")
    results = model.train(
        data='yolo_dataset',
        epochs=10,
        imgsz=128,
        batch=16,
        workers=2,
        project='runs/classify',
        name='train'
    )
    
    print("\nTraining completed!")
    
    # 3. Save best weights
    best_weights_path = 'runs/classify/train/weights/best.pt'
    target_weights_path = 'prakriti_yolo_model.pt'
    
    if os.path.exists(best_weights_path):
        shutil.copy(best_weights_path, target_weights_path)
        print(f"✅ Best weights saved to: {target_weights_path}")
    else:
        print("❌ Error: Best weights file not found!")
        
    print("=" * 60)

if __name__ == "__main__":
    main()
