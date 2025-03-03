from src.acquisition.data_loader import load_images
from src.reconstruction.sfm import run_sfm
from src.reconstruction.mvs import run_mvs
from src.hazard_detection.model import HazardDetectionNet
from src.hazard_detection.inference import predict_hazards
import open3d as o3d
import torch
import numpy as np

def run_pipeline():
    # 1. Data Acquisition: Load images from data/raw
    print("Loading images...")
    images = load_images("data/raw")
    if not images:
        print("No images found in data/raw. Please add sample images and try again.")
        return

    # 2. 3D Reconstruction: Run SfM to get dummy camera poses and sparse point cloud
    print("Running Structure-from-Motion...")
    camera_poses, sparse_point_cloud = run_sfm(images)
    
    # 3. Dense Reconstruction: Run MVS (dummy implementation)
    print("Running Multi-View Stereo reconstruction...")
    dense_model = run_mvs(sparse_point_cloud)
    
    # Visualize the 3D model if dense_model has data
    if dense_model and len(dense_model) > 0:
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(np.array(dense_model))
        o3d.visualization.draw_geometries([pcd])
    
    # 4. Hazard Detection: Create dummy 3D volume and run inference
    input_volume = torch.randn(1, 1, 32, 32, 32)  # Replace with actual volume conversion later
    model = HazardDetectionNet(input_channels=1)
    predicted_class, predicted_coords = predict_hazards(model, input_volume)
    
    print("Hazard Detection Results:")
    print("Predicted class (0: no hazard, 1: hazard):", predicted_class)
    print("Predicted hazard coordinates:", predicted_coords)

if __name__ == "__main__":
    run_pipeline()
