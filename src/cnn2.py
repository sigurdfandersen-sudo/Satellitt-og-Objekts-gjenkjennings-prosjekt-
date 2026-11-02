print("STARTER PROGRAM. HENT POPCORN!")

from PIL import Image
import json #tekstformat for å lagre strukturerte data, HRSID bruker det for å beskrive bilder og båter
from PIL import Image, ImageDraw
from pathlib import Path
import random
import shutil

treningbilder_liste = []
valideringsbilder_liste = []
testbilder_liste = []

with open("data/raw/HRSID_JPG/annotations/train_test2017.json", encoding = "utf-8") as fil:
    fasit_alle = json.load(fil) #python ordboken laget fra JSON fasit filen, ikke selve filen

with open("data/raw/bildelister/treningsbilderliste.txt", "r", encoding= "utf-8") as fil:
    for linje in fil:
        linje = linje.strip()
        treningbilder_liste.append(linje)

bilde_navn = treningbilder_liste[0]
for fasit in fasit_alle["images"]:
    if fasit["file_name"] == bilde_navn:
        print(fasit["id"])

print(f"antall treningsbilder er {len(treningbilder_liste)}")
print(treningbilder_liste[0])


