print("STARTER PROGRAM. HENT POPCORN!")
import torch
import numpy as np
import matplotlib as plt
from ultralytics import YOLO #Ultralytics driver med computer vision og YOLO(you only look once) er en objekt gjenkjenning/deteksjons model
from PIL import Image
import json #tekstformat for å lagre strukturerte data, HRSID bruker det for å beskrive bilder og båter


modell = YOLO("models/yolo26n.pt") #model med ferdigtrente vekter, 
bilde = Image.open("data/raw/HRSID_JPG/JPEGImages/P0001_1200_2000_0_800.jpg")

resultater = modell.predict(source=bilde, save = True)
print(bilde.size)
print(bilde.mode)

with open(
    "data/raw/HRSID_JPG/annotations/train_test2017.json", 
    encoding = "utf-8"
) as fil:
    fasit = json.load(fil)

print(fasit.keys())

bilde.show("første bilde")
print(fasit["images"][0])
print(fasit["annotations"][0])
print(fasit["annotations"][0]["bbox"])