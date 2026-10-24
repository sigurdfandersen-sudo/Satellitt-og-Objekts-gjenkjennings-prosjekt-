print("STARTER PROGRAM. HENT POPCORN!")
import torch
import numpy as np
import matplotlib as plt
from ultralytics import YOLO #Ultralytics driver med computer vision og YOLO(you only look once) er en objekt gjenkjenning/deteksjons model
from PIL import Image
import json #tekstformat for å lagre strukturerte data, HRSID bruker det for å beskrive bilder og båter
from PIL import Image, ImageDraw
from pathlib import Path


with open(
    "data/raw/HRSID_JPG/annotations/train_test2017.json", 
    encoding = "utf-8"
) as fil:
    fasit = json.load(fil) #python ordboken laget fra JSON fasit filen, ikke selve filen

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
