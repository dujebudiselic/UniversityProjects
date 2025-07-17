import tkinter as tk
from tkinter import filedialog
from tkinter import Label
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('PrometniZnakoviModel.keras')

popis_znakova = {
    0: 'Ograničenje brzine (20 km/h)',
    1: 'Ograničenje brzine (30 km/h)',
    2: 'Ograničenje brzine (50 km/h)',
    3: 'Ograničenje brzine (60 km/h)',
    4: 'Ograničenje brzine (70 km/h)',
    5: 'Ograničenje brzine (80 km/h)',
    6: 'Prestanak ograničenja brzine (80 km/h)',
    7: 'Ograničenje brzine (100 km/h)',
    8: 'Ograničenje brzine (120 km/h)',
    9: 'Zabrana pretjecanja svih motornih vozila osim motocikla bez prikolice i mopeda',
    10: 'Zabrana pretjecanja za teretne automobile',
    11: 'Raskrižje sa sporednom cestom pod pravim kutom',
    12: 'Cesta s prednošću prolaska',
    13: 'Raskrižje s cestom koja ima prednost prolaza',
    14: 'Obvezno zaustavljanje',
    15: 'Zabrana prometa u oba smjera',
    16: 'Zabrana prometa za teretne automobile',
    17: 'Zabrana prometa u jednom smjeru',
    18: 'Opasnost na cesti',
    19: 'Zavoj ulijevo',
    20: 'Zavoj udesno',
    21: 'Dvostruki zavoj',
    22: 'Neravan kolnik',
    23: 'Sklizak kolnik',
    24: 'Cesta se sužava s desne strane',
    25: 'Radovi na cesti',
    26: 'Nailazak na prometna svjetla',
    27: 'Obilježen pješački prelaz',
    28: 'Djeca na cesti',
    29: 'Biciklisti na cesti',
    30: 'Poledica',
    31: 'Divljač na cesti',
    32: 'Prestanak svih zabrana',
    33: 'Obvezan smjer desno',
    34: 'Obvezan smjer lijevo',
    35: 'Obvezan smjer ravno',
    36: 'Dopušteni smjerovi ravno ili desno',
    37: 'Dopušteni smjerovi ravno ili lijevo',
    38: 'Obvezno obilaženje s desne strane',
    39: 'Obvezno obilaženje s lijeve strane',
    40: 'Kružni tok prometa',
    41: 'Prestanak zabrane pretjecanja svih motornih vozila osim mopeda',
    42: 'Prestanak zabrane pretjecanja za teretne automobile'
}

def predict(path):
    slika = Image.open(path).convert('RGB')
    slika = slika.resize((60, 60))
    slika = np.array(slika)
    slika = np.expand_dims(slika, axis=0)

    predikcija = model.predict(slika)
    klasa = np.argmax(predikcija)
    return popis_znakova[klasa]


def upload():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if not file_path:
        return

    img = Image.open(file_path).convert('RGB')
    img = img.resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)

    prozor.config(width=200, height=200)
    prozor.configure(image=img_tk, text="")
    prozor.image = img_tk

    rez = predict(file_path)
    rez_label.config(text=rez)


def show_info_page():
    main_frame.pack_forget()
    info_frame.pack()

def show_main_page():
    info_frame.pack_forget()
    main_frame.pack(fill='both', expand=True)

ekran = tk.Tk()
ekran.title("Klasifikacija slika prometnih znakova")

ekran.geometry("850x650")
ekran.config(bg="#f0f0f0")
ekran.resizable(False, False)


main_frame = tk.Frame(ekran, bg="white")
main_frame.pack(fill='both', expand=True)


info_btn = tk.Button(main_frame, text="INFO", command=show_info_page, font=("Helvetica", 12), bg="#66BB6A", fg="white", relief="raised", bd=2)
info_btn.place(x=750, y=10)

odabir_ima_label = tk.Label(main_frame, text="Odaberite sliku prometnog znaka", font=("Helvetica", 14, "bold"), bg="white")
odabir_ima_label.pack(pady=20)

prozor = Label(main_frame, text="Nema slike", width=20, height=10, relief="solid", anchor="center", font=("Helvetica", 12), bg="lightgray")
prozor.pack(pady=20)

upload_btn = tk.Button(main_frame, text="Učitaj sliku", command=upload, width=18, font=("Helvetica", 12), bg="#008CBA", fg="white", relief="raised", bd=2)
upload_btn.pack(pady=20)


rez_label = tk.Label(main_frame, font=("Helvetica", 14), bg="white", fg="#003366")
rez_label.pack(pady=20)


info_frame = tk.Frame(ekran, bg="#f0f0f0")

info_text = """
Naziv projekta: Računalni vid - klasifikacija slika prometnih znakova

Opis:
Tema projekta je upotrijebiti nadzirano učenje za treniranje neuronske mreže na 
problemu klasifikacije slika prometnih znakova. Za to je korišten programski jezik Python 
i biblioteka TensorFlow. Odabrana je ova tema jer je primjenjiva u današnjem svijetu 
(samovozeći auti moraju detektirati i prepoznavati prometne znakove).

Korištenje:
U aplikaciju je ugradena istrenirana neuronska mreža. Korisnik samo mora odabirom 
"Učitaj sliku" odabrati sliku, a model će pokušati dati točno ime znaka sa slike.

Mentor:
Izv. prof. dr. sc. Tomislav Hrkać

Studenti:
- Viktor Bogojević
- Duje Budiselić
- Josip Grgić
- Petar Knežević
- Mislav Markušić
"""
back_btn = tk.Button(info_frame, text="Povratak", command=show_main_page, font=("Helvetica", 12))
back_btn.pack(side="top", pady=20)

# Labela koja prikazuje tekst info kartice
info_label = tk.Label(info_frame, text=info_text, font=("Helvetica", 12), justify="left", bg="#f0f0f0")
info_label.pack(padx=20, pady=20)

# Dodavanje copyright-a u donji dio
copyright_label = tk.Label(ekran, text="© 2025 Projekt R, Grupa 117", font=("Helvetica", 10), bg="#f0f0f0")
copyright_label.pack(side="bottom", pady=10)

ekran.mainloop()