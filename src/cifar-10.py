import torch.optim as optim
import torchvision
print("STARTER PROGRAM. HENT POPCORN")
import torch
import numpy as np
import matplotlib as plt
import torch.nn as nn
from pathlib import Path
from PIL import Image
from torchvision.transforms.functional import to_tensor
import torch.nn.functional as F

class Net(nn.Module): #definerer type objekt, Net får egenskaper og støte fra nn.Module. Objekt er en konkret ting med egen data, handlinger tilknyttet seg, klassen er som en oppskrift for handlinger og håndtering
    def __init__(self):#_init_ er metoden som kjøres, self viser til dette modellobjektet, self betyr dette objektet inne i klassen
        super().__init__() #oppstart til foreldreklassen, torch håndtering av modellen, med lag, parametere, 
        self.Conv1 = nn.Conv2d(3, 6, 5) #3 inngangskanaler (RGB), 6 filtre, 5 * 5 kernel size, med ulike filtervekter og en bias, mister piksler, siden vi har ingen kantutfylling
        self.pool = nn.MaxPool2d(2, 2) #ser på 2x2 verdier og beholder den største, så tar den 2 steg om gangen, bredde og høyde halvert, komprimerer resultat kartet
        self.Conv2 = nn.Conv2d(6, 16, 5) #tar inn 6 verdier fra 6 verdiene i forrige konvulusjonslag(resultatkart), lager 16 nye filtre mde 5x5 kernel størrelse, form(16, 10, 10)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.Conv1(x))) #først konvolusjonslag, der vi får 6 filteverdier, så 
        x = self.pool(F.relu(self.Conv2(x)))
        x = torch.flatten(x, 1) #vi skal flate ut alle verdier i denne batchen, men vi bruker lister,
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)



modell = Net() #her blir objektet(nettverket) opprettet etter beskrivelsen ovenfor
