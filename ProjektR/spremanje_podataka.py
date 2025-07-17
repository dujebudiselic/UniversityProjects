import numpy as np
import os
from PIL import Image, ImageOps
from tqdm import tqdm

os.chdir('../prometni_znakovi')

podaci = []
broj_direktorija = []
broj_znakova = 43
path = os.getcwd()

for i in tqdm(range (broj_znakova)):
    train_path = path + '/Train/' + str(i)
    slike = os.listdir(train_path)
    for d in slike:
        try:
            slika = Image.open(train_path + '/' + d)
            slika = slika.resize((60, 60))
            slika = ImageOps.grayscale(slika)
            slika = np.array(slika)
            podaci.append(slika)
            broj_direktorija.append(i)
        except Exception as e:
            print(e)

podaci = np.array(podaci)

broj_direktorija = np.array(broj_direktorija)
print(podaci.shape, broj_direktorija.shape) #(39209, 60, 60) (39209,)

np.save("podaci",podaci)
np.save("broj_direktorija",broj_direktorija)
