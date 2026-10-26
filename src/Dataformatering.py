print("STARTER PROGRAM. HENT POPCORN!")

from PIL import Image
import json #tekstformat for å lagre strukturerte data, HRSID bruker det for å beskrive bilder og båter
from PIL import Image, ImageDraw
from pathlib import Path
import random
import shutil 


with open("data/raw/HRSID_JPG/annotations/train_test2017.json", encoding = "utf-8") as fil:
    fasit_validering = json.load(fil) #python ordboken laget fra JSON fasit filen, ikke selve filen

with open("data/raw/HRSID_JPG/annotations/train2017.json", encoding= "utf-8") as fil:
    fasit_trening = json.load(fil) 

with open("data/raw/HRSID_JPG/annotations/test2017.json", encoding= "utf-8") as fil:
    fasit_testing = json.load(fil) 



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

def lagre_etiketter_validering(filnavn, info):
    etikettfil_navn = Path(filnavn).stem + ".txt"
    with open(
        f"data/processed/labels/validering/{etikettfil_navn}",#finner eller lager og åpner filen
        "w",
        encoding= "utf-8",
    )as etikkettefil: #gir python et filobjekt, med navn etikettefil som kan brukes lokalt i funksjonen
        for båt in info:
            linje = f"{båt['klasse']} {båt['midt_x']} {båt['midt_y']} {båt['boks_bredde']} {båt['boks_høyde']}\n"
            etikkettefil.write(linje)

def lagre_etiketter_trening(filnavn, info):
    etikettfil_navn = Path(filnavn).stem + ".txt"
    with open(
        f"data/processed/labels/trening/{etikettfil_navn}",#finner eller lager og åpner filen
        "w",
        encoding= "utf-8",
    )as etikkettefil: #gir python et filobjekt, med navn etikettefil som kan brukes lokalt i funksjonen
        for båt in info:
            linje = f"{båt['klasse']} {båt['midt_x']} {båt['midt_y']} {båt['boks_bredde']} {båt['boks_høyde']}\n"
            etikkettefil.write(linje)

def lagre_etiketter_testing(filnavn, info):
    etikettfil_navn = Path(filnavn).stem + ".txt"
    with open(
        f"data/processed/labels/testing/{etikettfil_navn}",#finner eller lager og åpner filen
        "w",
        encoding= "utf-8",
    )as etikkettefil: #gir python et filobjekt, med navn etikettefil som kan brukes lokalt i funksjonen
        for båt in info:
            linje = f"{båt['klasse']} {båt['midt_x']} {båt['midt_y']} {båt['boks_bredde']} {båt['boks_høyde']}\n"
            etikkettefil.write(linje)

for bilde in fasit_validering["images"]:
    filnavn = bilde["file_name"]
    info = konverter_bilde(filnavn, fasit_validering)
    lagre_etiketter_validering(filnavn, info)

for bilde in fasit_trening["images"]:
    filnavn = bilde["file_name"]
    info = konverter_bilde(filnavn, fasit_trening)
    lagre_etiketter_trening(filnavn, info)

for bilde in fasit_testing["images"]:
    filnavn = bilde["file_name"]
    info = konverter_bilde(filnavn, fasit_testing)
    lagre_etiketter_testing(filnavn, info)

kilde_ider = set()
kilde_liste = []
treningbilder_liste = []
valideringsbilder_liste = []
testbilder_liste = []

for bilde in fasit_validering["images"]:
    kilde_id = bilde["file_name"].split("_")[0]
    kilde_ider.add(kilde_id)


kilde_liste = sorted(kilde_ider)
trekning = random.Random(42)
trekning.shuffle(kilde_liste)

trening_ider = kilde_liste[:96]
validering_ider = kilde_liste[96:116]
test_ider = kilde_liste[116:]

for bilde in fasit_["images"]:
    kilde_id = bilde["file_name"].split("_")[0]
    kilde_ider.add(kilde_id)

    if kilde_id in trening_ider:
        treningbilder_liste.append(bilde)
    elif kilde_id in validering_ider:
        valideringsbilder_liste.append(bilde)
    else:
        testbilder_liste.append(bilde)

with open("data/raw/bildelister/treningsbilderliste.txt", "w", encoding= "utf-8") as fil:
    for treningsbilde in treningbilder_liste:
        navn = treningsbilde["file_name"]
        fil.write(navn + "\n") 

with open("data/raw/bildelister/valideringsbilderliste.txt", "w", encoding= "utf-8") as fil:
    for valideringsbilde in valideringsbilder_liste:
        navn = valideringsbilde["file_name"]
        fil.write(navn + "\n") 

with open("data/raw/bildelister/testbilderliste.txt", "w", encoding= "utf-8") as fil:
    for testbilde in testbilder_liste:
        navn = testbilde["file_name"]
        fil.write(navn + "\n") 

for treningsbilde in treningbilder_liste:
    filnavn = treningsbilde["file_name"]
    shutil.copy2(f"data/raw/HRSID_JPG/JPEGImages/{filnavn}", f"data/processed/images/trening/{filnavn}")

for valideringsbilde in valideringsbilder_liste:
    filnavn = valideringsbilde["file_name"]
    shutil.copy2(f"data/raw/HRSID_JPG/JPEGImages/{filnavn}", f"data/processed/images/validering/{filnavn}")

for testbilde in testbilder_liste:
    filnavn = testbilde["file_name"]
    shutil.copy2(f"data/raw/HRSID_JPG/JPEGImages/{filnavn}", f"data/processed/images/testing/{filnavn}")


print("antall treningbilder er ", len(treningbilder_liste))
print("antall valideringsbilder er ", len(valideringsbilder_liste))
print("antall testbilder er ", len(testbilder_liste))

print("antall kilde_ider er ", len(kilde_ider))
print("antall trenings ider", len(trening_ider))
print("antall validerings ider", len(validering_ider))
print("antall test ider", len(test_ider))
print("antall bilder av test_trainer ", len(fasit["images"]))
print("antall bilder av test sett er", len(fasit_test["images"]))
print("antall bilder av trening sett er", len(fasit_trening["images"]))
print("de 5 første elementene i id er ", kilde_liste[:5])
print("de 5 siste elemente i id er ", kilde_liste[-5:])

