"""
Synthetic Dataset Generator for YOLOv8 Prakriti Classification
Generates stylized silhouette/color images for Vata, Pitta, and Kapha classes
"""

import os
import random
import numpy as np
from PIL import Image, ImageDraw

def create_stylized_image(dosha_class, size=(128, 128)):
    # Create background (random neutral light tone)
    bg_color = (
        random.randint(220, 245),
        random.randint(220, 245),
        random.randint(220, 245)
    )
    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Add random background noise/clutter
    for _ in range(random.randint(2, 6)):
        nx = random.randint(0, size[0])
        ny = random.randint(0, size[1])
        nr = random.randint(2, 8)
        draw.ellipse([nx-nr, ny-nr, nx+nr, ny+nr], fill=(random.randint(180, 210),)*3)
        
    w, h = size
    
    if dosha_class == 0:  # VATA (Tall, thin, dry/brownish/dark tones)
        # Dimensions: Narrow and elongated
        sw = random.randint(18, 30)
        sh = random.randint(85, 105)
        # Colors: Dark brown, grey, dry earthy tones
        color = (
            random.randint(90, 130), # R
            random.randint(70, 100),  # G
            random.randint(50, 80)    # B
        )
        
    elif dosha_class == 1:  # PITTA (Moderate, sharp, warm/reddish/bright tones)
        # Dimensions: Balanced athletic proportions
        sw = random.randint(38, 48)
        sh = random.randint(70, 85)
        # Colors: Flushed red, pink, warm orange/golden tones
        color = (
            random.randint(200, 240), # R (high red)
            random.randint(110, 150), # G (moderate)
            random.randint(90, 130)   # B (moderate)
        )
        
    else:  # KAPHA (Broad, round, heavy, pale/light/yellowish tones)
        # Dimensions: Wide and round/thick
        sw = random.randint(65, 85)
        sh = random.randint(60, 75)
        # Colors: Pale white, soft yellow, smooth ivory tones
        color = (
            random.randint(230, 255), # R
            random.randint(220, 245), # G
            random.randint(180, 210)  # B (yellowish hue)
        )
        
    # Draw body silhouette (centered with slight random offset)
    cx = w // 2 + random.randint(-5, 5)
    cy = h // 2 + random.randint(-5, 5)
    
    x1 = cx - sw // 2
    y1 = cy - sh // 2
    x2 = cx + sw // 2
    y2 = cy + sh // 2
    
    # Draw head
    hr = sw // 2
    hx = cx
    hy = y1 - hr // 3
    draw.ellipse([hx-hr, hy-hr, hx+hr, hy+hr], fill=color)
    
    # Draw body silhouette
    draw.ellipse([x1, y1, x2, y2], fill=color)
    
    # Add pixel noise to prevent overfitting
    arr = np.array(img)
    noise = np.random.randint(-15, 15, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(arr)

def main():
    print("=" * 60)
    print("Generating Synthetic Image Dataset for YOLO Classification")
    print("=" * 60)
    
    dataset_dirs = [
        'yolo_dataset/train/vata',
        'yolo_dataset/train/pitta',
        'yolo_dataset/train/kapha',
        'yolo_dataset/val/vata',
        'yolo_dataset/val/pitta',
        'yolo_dataset/val/kapha'
    ]
    
    # Create directories
    for directory in dataset_dirs:
        os.makedirs(directory, exist_ok=True)
        
    classes = ['vata', 'pitta', 'kapha']
    
    # Generate images
    # Train: 300 per class, Val: 100 per class (Total: 1200 images)
    train_count = 300
    val_count = 100
    
    print("Generating Training Set...")
    for idx, name in enumerate(classes):
        print(f" -> Class: {name} (Generating {train_count} images)")
        for i in range(train_count):
            img = create_stylized_image(idx)
            img.save(f"yolo_dataset/train/{name}/{name}_{i}.png")
            
    print("\nGenerating Validation Set...")
    for idx, name in enumerate(classes):
        print(f" -> Class: {name} (Generating {val_count} images)")
        for i in range(val_count):
            img = create_stylized_image(idx)
            img.save(f"yolo_dataset/val/{name}/{name}_{i}.png")
            
    print("\nDataset generation complete!")
    print("Train count: 900 images")
    print("Val count: 300 images")
    print("=" * 60)

if __name__ == "__main__":
    main()
