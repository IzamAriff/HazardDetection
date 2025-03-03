def run_sfm(images):
    """
    Dummy Structure-from-Motion (SfM) pipeline.
    In a real system, integrate with COLMAP or OpenMVG.
    
    Args:
        images (list): List of images (numpy arrays).

    Returns:
        camera_poses: List of dummy camera poses.
        sparse_point_cloud: Dummy sparse 3D point cloud.
    """
    print("Running dummy SfM on {} images...".format(len(images)))
    # Dummy camera poses (None) and empty sparse point cloud
    camera_poses = [None] * len(images)
    sparse_point_cloud = []  # Replace with actual 3D points from SfM.
    return camera_poses, sparse_point_cloud
