from src.acquisition.data_loader import load_images
from src.reconstruction.sfm import run_sfm
from src.reconstruction.mvs import run_mvs
from src.hazard_detection.model import HazardDetectionNet
from src.hazard_detection.inference import predict_hazards
import open3d as o3d
import torch
import numpy as np

def run_pipeline():
    # Step 1: Data Acquisition
    print("Loading images from data/raw...")
    images, image_files = load_images("data/raw")
    if not images:
        print("No images found in data/raw. Please add sample images and try again.")
        return

    # Step 2: 3D Reconstruction using COLMAP (SfM)
    print("Running SfM reconstruction using COLMAP...")
    model_dir, sparse_ply = run_sfm("data/raw")
    
    # Visualize the sparse point cloud
    print("Loading and visualizing sparse point cloud...")
    pcd_sparse = o3d.io.read_point_cloud(sparse_ply)
    o3d.visualization.draw_geometries([pcd_sparse], window_name="Sparse Point Cloud")

    # Step 3: Dense Reconstruction (MVS)
    print("Running dense reconstruction (MVS) using COLMAP...")
    dense_ply = run_mvs(model_dir, "data/raw")
    
    # Visualize the dense point cloud
    print("Loading and visualizing dense point cloud...")
    pcd_dense = o3d.io.read_point_cloud(dense_ply)
    o3d.visualization.draw_geometries([pcd_dense], window_name="Dense Point Cloud")

    # Step 4: Hazard Detection
    # For demonstration, we convert the dense point cloud to a voxel grid.
    # In a real application, you'd convert your 3D model into the format expected by your ML model.
    print("Converting dense point cloud to voxel grid for ML input...")
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd_dense, voxel_size=0.1)
    # For simplicity, we will create a dummy 3D tensor from the voxel grid.
    # (This is a placeholder – replace with your actual volume conversion.)
    dummy_volume = torch.randn(1, 1, 32, 32, 32)

    print("Running hazard detection inference...")
    model = HazardDetectionNet(input_channels=1)
    # Ideally, you would load a trained model checkpoint here.
    predicted_class, predicted_coords = predict_hazards(model, dummy_volume)
    
    print("\nHazard Detection Results:")
    print("Predicted class (0: no hazard, 1: hazard):", predicted_class)
    print("Predicted hazard coordinates:", predicted_coords)
    
    # Optionally, visualize hazard location on the dense model if coordinates make sense.
    # For now, we'll assume dummy coordinates.
    # Convert point cloud to numpy array:
    dense_points = np.asarray(pcd_dense.points)
    try:
        from src.utils.visualization import plot_hazard_on_model
        plot_hazard_on_model(dense_points, predicted_coords)
    except Exception as e:
        print("Visualization skipped due to error:", e)

if __name__ == "__main__":
    run_pipeline()
