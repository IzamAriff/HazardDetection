import cv2
import os

def load_images(image_dir):
    """
    Load images from the given directory.
    Returns a list of images (as numpy arrays in RGB format).
    """
    image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    images = []
    for file in image_files:
        img = cv2.imread(file)
        if img is not None:
            # Convert BGR (OpenCV default) to RGB
            images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    print(f"Loaded {len(images)} images from {image_dir}")
    return images
