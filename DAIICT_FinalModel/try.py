import torch

if torch.cuda.is_available():
    cuda_version = torch.version.cuda
    device_type = "GPU"
else:
    cuda_version = "Not available"
    device_type = "CPU"

print(f"CUDA {cuda_version} + {device_type}")
