import os
import subprocess
import shutil

def run_mvs(model_dir, image_dir, output_dir="data/processed/mvs_output"):
    """
    Runs COLMAP's dense reconstruction (MVS) pipeline on an existing SfM model.
    This calls COLMAP's patch_match_stereo and stereo_fusion commands.
    
    Args:
        model_dir (str): Directory containing the SfM model.
        image_dir (str): Directory containing raw images.
        output_dir (str): Directory where the dense reconstruction output will be stored.
    
    Returns:
        fused_ply (str): Path to the fused dense point cloud (PLY format).
    """
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Run COLMAP patch_match_stereo on the SfM workspace.
    cmd_patch = [
        "colmap", "patch_match_stereo",
        "--workspace_path", model_dir,
        "--workspace_format", "COLMAP",
        "--PatchMatchStereo.geom_consistency", "true"
    ]
    print("Running COLMAP patch_match_stereo...")
    subprocess.run(cmd_patch, check=True)
    
    # Run COLMAP stereo_fusion to fuse the dense stereo results into a point cloud.
    fused_ply = os.path.join(output_dir, "fused.ply")
    cmd_fusion = [
        "colmap", "stereo_fusion",
        "--workspace_path", model_dir,
        "--workspace_format", "COLMAP",
        "--input_type", "photometric",
        "--output_path", fused_ply,
        "--max_image_size", "2000"
    ]
    print("Running COLMAP stereo_fusion...")
    subprocess.run(cmd_fusion, check=True)
    
    print(f"Dense reconstruction complete. Fused point cloud at: {fused_ply}")
    return fused_ply
