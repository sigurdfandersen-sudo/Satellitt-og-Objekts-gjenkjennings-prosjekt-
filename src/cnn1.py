print("STARTER PROGRAM. HENT POPCORN")
import torch
import numpy as np
import matplotlib as plt
import torch.nn as nn
from pathlib import Path
from PIL import Image
from torchvision.transforms.functional import to_tensor

gpu = torch.device("cuda")

bs = 64 #batch size/ batchstørrelse

filsti = "data/raw/HRSID_JPG/JPEGImages/P0001_0_800_10190_10990.jpg"
bilde = Image.open(filsti)
bilde.show(title="første bilde")

bilde_tensor = to_tensor(bilde)
bilde_flat = torch.flatten(bilde_tensor)
print("Bilde størrelse er ", bilde.size)
print("bilde modus er ", bilde.mode)
print("bilde tensor er ", bilde_tensor)
print("bilde tensor form er ", bilde_tensor.shape)

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv2d = nn.Conv2d

modell = Net()
        
