print("STARTER PROGRAM. HENT POPCORN!")

from PIL import Image
import json #tekstformat for å lagre strukturerte data, HRSID bruker det for å beskrive bilder og båter
from PIL import Image, ImageDraw
from pathlib import Path
import random
import shutil
import torch
from torchvision.transforms.functional import to_tensor
import random
from torch.utils.data import Dataset



treningbilder_liste = []
valideringsbilder_liste = []
testbilder_liste = []
antall_båter = 0
båt_liste_markering = []
areal_liste = []
iscrowd_liste = []
bilde_nr = random.randint(0, 3879)

with open("data/raw/HRSID_JPG/annotations/train_test2017.json", encoding = "utf-8") as fil:
    fasit_alle = json.load(fil) #python ordboken laget fra JSON fasit filen, ikke selve filen

with open("data/raw/bildelister/treningsbilderliste.txt", "r", encoding= "utf-8") as fil:
    for linje in fil:
        linje = linje.strip()
        treningbilder_liste.append(linje)


bilde_navn = treningbilder_liste[bilde_nr]

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
                areal_liste.append(båt_info["area"])
                iscrowd_liste.append(båt_info["iscrowd"])

klasse_verdi_liste = torch.ones(antall_båter, dtype=torch.int64)
båt_liste_markering = torch.tensor(båt_liste_markering, dtype = torch.float32)
areal_liste = torch.tensor(areal_liste, dtype=torch.float32)
iscrowd_liste = torch.tensor(iscrowd_liste, dtype=torch.int64)

target = {
    "image_id":bilde_id,
    "boxes":båt_liste_markering,
    "labels":klasse_verdi_liste,
    "area":areal_liste,
    "iscrowd":iscrowd_liste
    }


filsti = Path("data/processed/images/trening") / bilde_navn
bilde = Image.open(filsti)
bilde_tensor  = to_tensor(bilde)

eksempel = bilde_tensor, target

class HRSIDDataset(Dataset):
    def __init__(self):
        self.datasett = treningbilder_liste

    def __len__(self):
        return len(self.datasett)





        
        return 


print(f"antall treningsbilder er {len(treningbilder_liste)}")
print(treningbilder_liste[0])
print(f"antall båter er {antall_båter}")
print(båt_liste_markering.shape)
print(len(båt_liste_markering[0]))

print("target[boxes] shape er ", target["boxes"].shape)
print("target[labels] shape er ", target["labels"].shape)
print("target[iscrowd] shape er ", target["iscrowd"].shape)
print("target[area] shape er ", target["area"].shape)

print(bilde_id)
print(target["image_id"])
print(iscrowd_liste)
print(f"bilde_tensor shape er {bilde_tensor.shape}")
print(f"bilde_navn er {bilde_navn}")