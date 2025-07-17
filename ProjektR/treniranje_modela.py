import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as ts
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout
from PIL import Image, ImageOps
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

def testing(testcsv):
    y_test = pd.read_csv(testcsv)
    broj_direktorija_test = y_test["ClassId"].values
    slike_test = y_test["Path"].values
    podaci_test = []
    for b in slike_test:
        slika_test = Image.open(b)
        slika_test = slika_test.resize((60,60))
        slika_test = ImageOps.grayscale(slika_test)
        slika_test = np.array(slika_test)
        podaci_test.append(slika_test)
    X_test=np.array(podaci_test)
    return X_test, broj_direktorija_test

os.chdir('../promenti_znakovi')

#ucitavanje spremljenih podataka:
podaci=np.load('podaci.npy')
broj_direktorija=np.load('broj_direktorija.npy')

# dijelimo podatke na train i test
X_train, X_test, y_train, y_test = train_test_split(podaci, broj_direktorija, test_size=0.2, random_state=11)

# Pretvaranje 1-dimenzionalne nizove klasa u 43-dimenzionalne matrice klasa
y_train = to_categorical(y_train, 43)
y_test = to_categorical(y_test, 43)

model = Sequential()

model.add(Conv2D(32, (5,5), activation='relu', input_shape = (60, 60, 1)))
model.add(Conv2D(32, (5,5), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
#print(model.output_shape)

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
#print(model.output_shape)

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
#print(model.output_shape)

model.add(Dense(43, activation='softmax'))
#print(model.output_shape)

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

a = model.fit(X_train, y_train, batch_size=32, epochs=20, validation_data=(X_test, y_test))

X_test, broj_direktorija_test = testing('Test.csv')
Y_pred = np.argmax(model.predict(X_test), axis=-1)
conf_matrix = confusion_matrix(broj_direktorija_test, Y_pred)

# matrica zabune
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=np.unique(broj_direktorija_test))
disp.plot(cmap='viridis')
plt.show()

print(accuracy_score(broj_direktorija_test, Y_pred))

model.save("PrometniZnakoviModel.keras")