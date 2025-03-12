import os
import subprocess
import shutil

def run_sfm(image_dir, output_dir="data/processed/sfm_output", database_path="data/processed/sfm_database.db"):
    """
    Runs COLMAP's SfM pipeline to generate a sparse 3D reconstruction.
    Assumes COLMAP is installed and available in PATH.
    
    Args:
        image_dir (str): Directory containing raw images.
        output_dir (str): Where to write the SfM model.
        database_path (str): Path to the COLMAP database.
        
    Returns:
        model_dir (str): Path to the folder containing the reconstructed model.
        ply_output (str): Path to the generated PLY point cloud file.
    """
    # Clear previous outputs if necessary.
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    if os.path.exists(database_path):
        os.remove(database_path)

    # Run COLMAP feature extraction.
    cmd_feature = [
        "colmap", "feature_extractor",
        "--database_path", database_path,
        "--image_path", image_dir
    ]
    print("Running feature extraction...")
    subprocess.run(cmd_feature, check=True)

    # Run COLMAP exhaustive matcher.
    cmd_match = [
        "colmap", "exhaustive_matcher",
        "--database_path", database_path
    ]
    print("Running feature matching...")
    subprocess.run(cmd_match, check=True)

    # Run COLMAP mapper.
    cmd_mapper = [
        "colmap", "mapper",
        "--database_path", database_path,
        "--image_path", image_dir,
        "--output_path", output_dir
    ]
    print("Running mapper (SfM reconstruction)...")
    subprocess.run(cmd_mapper, check=True)

    # Identify the model directory.
    model_dirs = [os.path.join(output_dir, d) for d in os.listdir(output_dir)
                  if os.path.isdir(os.path.join(output_dir, d))]
    if not model_dirs:
        raise Exception("No reconstruction model found in SfM output.")
    model_dir = model_dirs[0]

    # Rename the folder if its name is "0".
    if os.path.basename(model_dir) == "0":
        new_model_dir = os.path.join(output_dir, "model_0")
        print(f"Renaming model folder '{model_dir}' to '{new_model_dir}'...")
        os.rename(model_dir, new_model_dir)
        model_dir = new_model_dir

    print("Using model directory:", model_dir)
    print("Contents:", os.listdir(model_dir))

    # Convert COLMAP model to PLY format.
    ply_output = os.path.join(model_dir, "points3D.ply")
    cmd_converter = [
        "colmap", "model_converter",
        "--input_path", model_dir,
        "--output_path", model_dir,
        "--output_type", "PLY"
    ]
    print("Converting model to PLY format...")
    subprocess.run(cmd_converter, check=True)

    print(f"SfM reconstruction complete. PLY file at: {ply_output}")
    return model_dir, ply_output
