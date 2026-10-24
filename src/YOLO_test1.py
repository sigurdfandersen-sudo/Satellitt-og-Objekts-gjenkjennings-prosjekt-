print("STARTER PROGRAM. HENT POPCORN!")
import torch
import numpy as np
import matplotlib as plt
from ultralytics import YOLO #Ultralytics driver med computer vision og YOLO(you only look once) er en objekt gjenkjenning/deteksjons model
modell = YOLO("models/yolo26s.pt")
