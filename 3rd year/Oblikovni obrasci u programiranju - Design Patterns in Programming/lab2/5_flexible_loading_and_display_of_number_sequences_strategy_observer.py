from abc import ABC, abstractmethod
import datetime
import time


class izvorbrojeva(ABC):
    @abstractmethod
    def generiraj(self):
        pass

class TipkovnickiIzvor(izvorbrojeva):
    def generiraj(self):
        try:
            broj = int(input('Unesite broj: '))
            if broj < 0:
                return -1
            return broj
        except ValueError:
            return -1


class DatotecniIzvor(izvorbrojeva):
    def __init__(self, datoteka):
        self.datoteka = open(datoteka, 'r', encoding='utf-8')

    def generiraj(self):
        linija = self.datoteka.readline()
        if linija:
            broj = int(linija.strip())
            if broj < 0:
                return -1
            return broj
        else:
            return -1

class akcije(ABC):
    @abstractmethod
    def izvediakciju(self, brojevi):
        pass

class zapisudatoteci(akcije):
    def izvediakciju(self, brojevi):
        with open('petizad.txt', 'a') as f:
            f.write(f"{datetime.datetime.now()} - {brojevi}\n")

class ispissume(akcije):
    def izvediakciju(self, brojevi):
        suma = 0
        for broj in brojevi:
            suma = suma + broj
        print('Suma brojeva:', suma)


class ispisprosjek(akcije):
    def izvediakciju(self, brojevi):
        suma = 0
        for broj in brojevi:
            suma = suma + broj
        if len(brojevi) > 0:
            prosjek = suma / len(brojevi)
            print('Prosjek brojeva:', prosjek)
        else:
            print('Nema brojeva pa bi dijeljenje s 0 javilo error')

class ispismedijan(akcije):
    def izvediakciju(self, brojevi):
        if len(brojevi) > 0:
            brojevi = sorted(brojevi)
            n = len(brojevi)
            srednji = int(n / 2)

            if n % 2 == 1:
                medijan = brojevi[srednji]
                print('Medijan brojeva:', medijan)
            else:
                medijan = (brojevi[srednji - 1] + brojevi[srednji]) / 2
                print('Medijan brojeva:', medijan)
        else:
            print('Nema brojeva pa bi dijeljenje s 0 javilo error')


class SlijedBrojeva:
    def __init__(self, izvor):
        self.izvor = izvor
        self.brojevi = []
        self.promatraci = []

    def setizvor(self, izvor):
        self.izvor = izvor

    def dodajakciju(self, akcija):
        self.promatraci.append(akcija)

    def izbrisiakciju(self, akcija):
        if akcija in self.promatraci:
            self.promatraci.remove(akcija)

    def obaviakcije(self):
        for akcija in self.promatraci:
            akcija.izvediakciju(self.brojevi)

    def kreni(self):
        while True:
            broj = self.izvor.generiraj()
            if broj == -1:
                break
            print('Učitan broj:', broj)
            self.brojevi.append(broj)
            self.obaviakcije()
            print()
            time.sleep(1)


izvor = TipkovnickiIzvor()
slijed = SlijedBrojeva(izvor)

akcija1 = zapisudatoteci()
akcija2 = ispissume()
akcija3 = ispisprosjek()
akcija4 = ispismedijan()
slijed.dodajakciju(akcija1)
slijed.dodajakciju(akcija2)
slijed.dodajakciju(akcija3)
slijed.dodajakciju(akcija4)

slijed.kreni()

izvor2 = DatotecniIzvor('5zadcitanje.txt')
slijed.setizvor(izvor2)

slijed.kreni()

slijed.izbrisiakciju(akcija2)
slijed.setizvor(izvor)

slijed.kreni()


