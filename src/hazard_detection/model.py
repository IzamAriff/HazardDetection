import torch
import torch.nn as nn

class HazardDetectionNet(nn.Module):
    def __init__(self, input_channels=1, num_classes=2):
        super(HazardDetectionNet, self).__init__()

        # A simple 3D CNN architecture for demonstration.
        self.conv1 = nn.Conv3d(input_channels, 8, kernel_size=3, padding=1)
        self.pool = nn.MaxPool3d(2)
        self.conv2 = nn.Conv3d(8, 16, kernel_size=3, padding=1)

        # Assume input 32x32x32 becomes 8x8x8 after pooling twice.
        self.fc1 = nn.Linear(16 * 8 * 8 * 8, 64)
        
        # Two outputs: one for classification, one for regression (hazard coordinates)
        self.fc_class = nn.Linear(64, num_classes)
        self.fc_reg = nn.Linear(64, 3)
        
    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        class_out = self.fc_class(x)
        reg_out = self.fc_reg(x)
        return class_out, reg_out

if __name__ == "__main__":
    # Quick test of the network with a dummy input.
    model = HazardDetectionNet(input_channels=1)
    dummy_input = torch.randn(1, 1, 32, 32, 32)  # Batch size 1
    class_out, reg_out = model(dummy_input)
    print("Class output:", class_out)
    print("Regression output:", reg_out)
