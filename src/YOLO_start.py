print("STARTER PROGRAM. HENT POPCORN!")
import torch
import numpy as np
import matplotlib as plt
from ultralytics import YOLO #Ultralytics driver med computer vision og YOLO(you only look once) er en objekt gjenkjenning/deteksjons model
from PIL import Image
import json #tekstformat for å lagre strukturerte data, HRSID bruker det for å beskrive bilder og båter
from PIL import Image, ImageDraw


modell = YOLO("models/yolo26n.pt") #model med ferdigtrente vekter, 
bilde = Image.open("data/raw/HRSID_JPG/JPEGImages/P0001_0_800_10190_10990.jpg")

resultater = modell.predict(source=bilde, save = True)
print(bilde.size)
print(bilde.mode)

with open(
    "data/raw/HRSID_JPG/annotations/train_test2017.json", 
    encoding = "utf-8"
) as fil:
    fasit = json.load(fil)

print(fasit.keys())


print(fasit["images"][0])
print(fasit["annotations"][0])
print(fasit["annotations"][0]["bbox"])
print("---------------------------------------")
tegner = ImageDraw.Draw(bilde)

for bilder in fasit["images"]:
    if bilder["file_name"] == "JPEGImages/P0001_0_800_10190_10990.jpg":
        bilde_id == bilder["id"]
        for markering in fasit["annotations"]:
            if markering["image_id"] == bilde_id:



    for markering in fasit["annotations"]:
        if 


    if bilder["file_name"] == "JPEGImages/P0001_0_800_10190_10990.jpg":

    for markering in fasit["annotations"]:
        if markering["image_id"] == "JPEGImages/P0001_0_800_10190_10990.jpg":

            print(markering["bbox"])
            x_kordinat_1 = markering["bbox"][0]
            y_kordinat_1 = markering["bbox"][1]

            x_kordinat_2 = markering["bbox"][0] + markering["bbox"][2]
            y_kordinat_2 = markering["bbox"][1] + markering["bbox"][3]
            tegner.rectangle([(x_kordinat_1, y_kordinat_1), (x_kordinat_2, y_kordinat_2)], outline="red", width=2)


bilde.show("første bilde")
