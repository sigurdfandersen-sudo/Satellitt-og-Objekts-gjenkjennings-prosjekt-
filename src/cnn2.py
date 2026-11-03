print("STARTER PROGRAM. HENT POPCORN!")

from PIL import Image
import json #tekstformat for å lagre strukturerte data, HRSID bruker det for å beskrive bilder og båter
from PIL import Image, ImageDraw
from pathlib import Path
import random
import shutil
import torch

treningbilder_liste = []
valideringsbilder_liste = []
testbilder_liste = []
antall_båter = 0
båt_liste_markering = []
torch.tensor(båt_liste_markering, dtype = torch.float32)


with open("data/raw/HRSID_JPG/annotations/train_test2017.json", encoding = "utf-8") as fil:
    fasit_alle = json.load(fil) #python ordboken laget fra JSON fasit filen, ikke selve filen

with open("data/raw/bildelister/treningsbilderliste.txt", "r", encoding= "utf-8") as fil:
    for linje in fil:
        linje = linje.strip()
        treningbilder_liste.append(linje)

bilde_navn = treningbilder_liste[0]
for bilde_info in fasit_alle["images"]:
    if bilde_info["file_name"] == bilde_navn:
        bilde_id = bilde_info["id"]
        for båt_info in fasit_alle["annotations"]:
            if båt_info["image_id"] == bilde_id:
                antall_båter += 1
                print(f"bbox er {båt_info["bbox"]}")
                x_min = båt_info["bbox"][0]
                y_min = båt_info["bbox"][1]
                x_max = båt_info["bbox"][0] + båt_info["bbox"][2]
                y_max = båt_info["bbox"][1] + båt_info["bbox"][3]
                båt_info_markering = [x_min, y_min, x_max, y_max]
                båt_liste_markering.append(båt_info_markering)
                båt_info_markering_t = torch.tensor(båt_info_markering, dtype= torch.float32)

        print(bilde_info["id"])

båt_liste_markering_t = torch.tensor(båt_liste_markering, dtype = torch.float32)

print(f"antall treningsbilder er {len(treningbilder_liste)}")
print(treningbilder_liste[0])
print(f"antall båter er {antall_båter}")
print(båt_liste_markering_t.shape)
print(len(båt_liste_markering_t[0]))

