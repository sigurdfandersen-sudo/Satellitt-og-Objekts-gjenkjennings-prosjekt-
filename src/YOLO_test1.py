print("STARTER PROGRAM. HENT POPCORN!")
from ultralytics import YOLO #Ultralytics driver med computer vision og YOLO(you only look once) er en objekt gjenkjenning/deteksjons model

modell = YOLO("models/yolo26s.pt")

modell.train(data="hrsid.yaml", epochs=80, imgsz = 800, batch = 8, device = 0, workers = 0, patience = 10)
