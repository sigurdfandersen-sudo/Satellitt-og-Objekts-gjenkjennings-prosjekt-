print("STARTER PROGRAM. HENT POPCORN!")

from PIL import Image
import json #tekstformat for å lagre strukturerte data, HRSID bruker det for å beskrive bilder og båter
from PIL import Image, ImageDraw
from pathlib import Path
import random


with open("data/raw/HRSID_JPG/annotations/train_test2017.json", encoding = "utf-8") as fil:
    fasit = json.load(fil) #python ordboken laget fra JSON fasit filen, ikke selve filen

with open("data/raw/HRSID_JPG/annotations/train2017.json", encoding= "utf-8") as fil:
    fasit_trening = json.load(fil) 

with open("data/raw/HRSID_JPG/annotations/test2017.json", encoding= "utf-8") as fil:
    fasit_test = json.load(fil) 



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

def lagre_etiketter_traintest(filnavn, info):
    etikettfil_navn = Path(filnavn).stem + ".txt"
    with open(
        f"data/processed/labels_traintest/{etikettfil_navn}",#finner eller lager og åpner filen
        "w",
        encoding= "utf-8",
    )as etikkettefil: #gir python et filobjekt, med navn etikettefil som kan brukes lokalt i funksjonen
        for båt in info:
            linje = f"{båt['klasse']} {båt['midt_x']} {båt['midt_y']} {båt['boks_bredde']} {båt['boks_høyde']}\n"
            etikkettefil.write(linje)

def lagre_etiketter_train(filnavn, info):
    etikettfil_navn = Path(filnavn).stem + ".txt"
    with open(
        f"data/processed/labels_train/{etikettfil_navn}",#finner eller lager og åpner filen
        "w",
        encoding= "utf-8",
    )as etikkettefil: #gir python et filobjekt, med navn etikettefil som kan brukes lokalt i funksjonen
        for båt in info:
            linje = f"{båt['klasse']} {båt['midt_x']} {båt['midt_y']} {båt['boks_bredde']} {båt['boks_høyde']}\n"
            etikkettefil.write(linje)

def lagre_etiketter_test(filnavn, info):
    etikettfil_navn = Path(filnavn).stem + ".txt"
    with open(
        f"data/processed/labels_test/{etikettfil_navn}",#finner eller lager og åpner filen
        "w",
        encoding= "utf-8",
    )as etikkettefil: #gir python et filobjekt, med navn etikettefil som kan brukes lokalt i funksjonen
        for båt in info:
            linje = f"{båt['klasse']} {båt['midt_x']} {båt['midt_y']} {båt['boks_bredde']} {båt['boks_høyde']}\n"
            etikkettefil.write(linje)

for bilde in fasit["images"]:
    filnavn = bilde["file_name"]
    info = konverter_bilde(filnavn, fasit)
    lagre_etiketter_traintest(filnavn, info)

for bilde in fasit_trening["images"]:
    filnavn = bilde["file_name"]
    info = konverter_bilde(filnavn, fasit_trening)
    lagre_etiketter_train(filnavn, info)

for bilde in fasit_test["images"]:
    filnavn = bilde["file_name"]
    info = konverter_bilde(filnavn, fasit_test)
    lagre_etiketter_test(filnavn, info)

kilde_ider = set()
kilde_liste = []
treningbilder_liste = []
valideringsbilder_liste = []
testbilder_liste = []

for bilde in fasit_trening["images"]:
    kilde_id = bilde["file_name"].split("_")[0]
    kilde_ider.add(kilde_id)
    kilde_liste = sorted(kilde_ider)
    trekning = random.Random(42)
    trekning.shuffle(kilde_liste)

    trening_ider = kilde_liste[:96]
    validering_ider = kilde_liste[96:116]
    test_ider = kilde_liste[116:]

    if kilde_id in trening_ider:
        treningbilder_liste.append(bilde)
    elif kilde_id in validering_ider:
        valideringsbilder_liste.append(bilde)
    else:
        testbilder_liste.append(bilde)


        
print("antall kilde_ider er ", len(kilde_ider))
print("antall trenings ider", len(trening_ider))
print("antall validerings ider", len(validering_ider))
print("antall test ider", len(test_ider))
print("antall bilder av test_trainer ", len(fasit["images"]))
print("antall bilder av test sett er", len(fasit_test["images"]))
print("antall bilder av trening sett er", len(fasit_trening["images"]))
print("de 5 første elementene i id er ", kilde_liste[:5])
print("de 5 siste elemente i id er ", kilde_liste[-5:])
