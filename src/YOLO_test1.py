print("STARTER PROGRAM. HENT POPCORN!")
import torch
import numpy as np
import matplotlib as plt
from ultralytics import YOLO #Ultralytics driver med computer vision og YOLO(you only look once) er en objekt gjenkjenning/deteksjons model

modell = YOLO("runs/detect/train-2/weights/best.pt")

modell.train(data="hrsid.yaml", epochs=5, imgsz = 800, batch = 2, device = 0, workers = 0)
