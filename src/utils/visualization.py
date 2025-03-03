import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_point_cloud(points):
    """
    Plot a 3D point cloud using matplotlib.
    
    Args:
        points: NumPy array of shape (N, 3)
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:,0], points[:,1], points[:,2], s=1)
    plt.title("3D Point Cloud")
    plt.show()

def plot_hazard_on_model(points, hazard_coords):
    """
    Plot the hazard point on a 3D point cloud.
    
    Args:
        points: NumPy array of shape (N, 3)
        hazard_coords: List or array [x, y, z]
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:,0], points[:,1], points[:,2], s=1, label="Model")
    ax.scatter(hazard_coords[0], hazard_coords[1], hazard_coords[2],
               color='r', s=50, label="Hazard")
    ax.legend()
    plt.title("Hazard on 3D Model")
    plt.show()
