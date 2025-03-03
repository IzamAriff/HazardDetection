import torch
from hazard_detection.model import HazardDetectionNet

def predict_hazards(model, input_volume):
    """
    Run hazard detection on an input 3D volume.
    
    Args:
        model: Trained hazard detection model.
        input_volume: Torch tensor of shape (1, channels, D, H, W).

    Returns:
        predicted_class: Integer (0 for no hazard, 1 for hazard).
        predicted_coords: List of three floats representing hazard location.
    """
    model.eval()
    with torch.no_grad():
        class_out, reg_out = model(input_volume)
        predicted_class = torch.argmax(class_out, dim=1).item()
        predicted_coords = reg_out.squeeze().cpu().numpy().tolist()
    return predicted_class, predicted_coords

if __name__ == "__main__":
    # Dummy inference test.
    model = HazardDetectionNet(input_channels=1)
    dummy_input = torch.randn(1, 1, 32, 32, 32)
    pred_class, pred_coords = predict_hazards(model, dummy_input)
    print("Predicted class:", pred_class)
    print("Predicted coordinates:", pred_coords)
