print("STARTER PROGRAM. HENT POPCORN!")
import torch
import numpy as np
import matplotlib as plt
from ultralytics import YOLO #Ultralytics driver med computer vision og YOLO(you only look once) er en objekt gjenkjenning/deteksjons model
from PIL import Image
import json #tekstformat for å lagre strukturerte data, HRSID bruker det for å beskrive bilder og båter
from PIL import Image, ImageDraw
from pathlib import Path

fil_navn = "P0001_3600_4400_4200_5000.jpg"
navn_uten_filtype = Path(fil_navn).stem
etikkete_navn = navn_uten_filtype + ".txt"
modell = YOLO("models/yolo26n.pt") #model med ferdigtrente vekter, 
bilde = Image.open(f"data/raw/HRSID_JPG/JPEGImages/{fil_navn}")

resultater = modell.predict(source=bilde, save = True)
print(bilde.size)
print(bilde.mode)

with open(
    "data/raw/HRSID_JPG/annotations/train_test2017.json", 
    encoding = "utf-8"
) as fil:
    fasit = json.load(fil)

print(fasit.keys())
bildets_bredde = 800
bildets_høyde = 800

print(fasit["images"][0])
print(fasit["annotations"][0])
print(fasit["annotations"][0]["bbox"])
print("---------------------------------------")
tegner = ImageDraw.Draw(bilde)
info = []

for bilder in fasit["images"]:
    if bilder["file_name"] == fil_navn:
        bilde_id = bilder["id"]
        for markering in fasit["annotations"]:
            if markering["image_id"] == bilde_id:
            
                
                print(markering["bbox"])
                x_kordinat_1 = markering["bbox"][0]
                y_kordinat_1 = markering["bbox"][1]
                x_kordinat_2 = markering["bbox"][0] + markering["bbox"][2]
                y_kordinat_2 = markering["bbox"][1] + markering["bbox"][3]
                tegner.rectangle([(x_kordinat_1, y_kordinat_1), (x_kordinat_2, y_kordinat_2)], outline="red", width=2)

                midt_x = x_kordinat_1 + markering["bbox"][2] / 2
                midt_y = y_kordinat_1 + markering["bbox"][3] / 2
                
                tegner.circle([midt_x, midt_y], radius = 10, width= 4, fill= "yellow")
                norm_midt_x = midt_x / bilder["width"]
                norm_midt_y = midt_y / bilder["height"]

                norm_boks_bredde = markering["bbox"][2] / bilder["width"]
                norm_boks_høyde = markering["bbox"][3] / bilder["height"]

                print("norm midt x er ", norm_midt_x)
                print("norm midt y er ", norm_midt_y)
                print("sentrum av boks er ", midt_x)
                print(midt_y)
                print("norm_boks_bredde = ", norm_boks_bredde)
                båt_info = {
                    "klasse": 0,
                    "midt_x": norm_midt_x,
                    "midt_y": norm_midt_y,
                    "boks_bredde": norm_boks_bredde,
                    "boks_høyde": norm_boks_høyde
                    }
                info.append(båt_info)        

for båt in info:
    print(båt["klasse"], båt["midt_x"], båt["midt_y"], båt["boks_bredde"], båt["boks_høyde"])



bilde.show("første bilde")
print(etikkete_navn)


with open( #åpner filen, hvis ikke finnes blir den opprettet, hvis filen finnes, tømmes innholdet, 
    f"data/processed/labels/{etikkete_navn}", #f string gjør at {} kan inneholde variabel, forteller hvor filen skal ligge
    "w",  #åpne for skriving
    encoding= "utf-8" #hvordan tekst oversettes til bytes
) as etikettfil: # gir filen et navn
    for båt in info:
        linje = f"{båt['klasse']} {båt['midt_x']} {båt['midt_y']} {båt['boks_bredde']} {båt['boks_høyde']}\n"
        etikettfil.write(linje)

def konverter_bilde(filnavn, fasit):
    info = []
    for bilder in fasit["images"]:
        if bilder["file_name"] == filnavn:
            bilde_id = bilder["id"]
            for markering in fasit["annotations"]:
                if markering["image_id"] == bilde_id:
                    x_kordinat_1 = markering["bbox"][0]
                    y_kordinat_1 = markering["bbox"][1]

                    midt_x = x_kordinat_1 + markering["bbox"][2] / 2
                    midt_y = y_kordinat_1 + markering["bbox"][3] / 2

                    norm_midt_x = midt_x / bilder["width"]
                    norm_midt_y = midt_y / bilder["height"]

                    norm_boks_bredde = markering["bbox"][2] / bilder["width"]
                    norm_boks_høyde = markering["bbox"][3] / bilder["height"]



                    båt_info = {
                        "klasse": 0,
                        "midt_x": norm_midt_x,
                        "midt_y": norm_midt_y,
                        "boks_bredde": norm_boks_bredde,
                        "boks_høyde": norm_boks_høyde
                    }
                    info.append(båt_info)
    return info

def lagre_etiketter(filnavn, info):
    etikettfil_navn = Path(filnavn).stem + ".txt"
    with open(
        f"data/processed/labels/{etikettfil_navn}",#finner eller lager og åpner filen
        "w",
        encoding= "utf-8",
    )as etikkettefil: #gir python et filobjekt, med navn etikettefil som kan brukes lokalt i funksjonen
        for båt in info:
            linje = f"{båt['klasse']} {båt['midt_x']} {båt['midt_y']} {båt['boks_bredde']} {båt['boks_høyde']}\n"
            etikkettefil.write(linje)










print("----------------------------------------")
info = konverter_bilde(fil_navn, fasit)
print(info)


