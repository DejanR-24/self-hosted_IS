'''
Ovaj IS predstavlja jednu Apoteku, sastoji se od klase Lijek,Zaposleni,Kasa i Apoteka
iscitava podatke iz dva json fajla koji predstavljaju spisak ljekova i spisak zaposlenih, svaka klasa posjeduje odredjene setere i getere i odredjene metode.

'''

from datetime import datetime
import six
import json
from copy import deepcopy
class Lijek:
    def __init__(self,naziv,proizvodjac,cijena,kolicina=1):
        self.naziv=naziv
        self.proizvodjac=proizvodjac
        self._cijena=cijena
        self._kolicina=kolicina
    def get_naziv(self):
        return self.naziv
    def get_proizvodjac(self):
        return self.proizvodjac
    def get_cijena(self):
        return self._cijena
    def get_kolicina(self):
        return self._kolicina
    def set_naziv(self,naziv):
        self.naziv=naziv
    def set_proizvodjac(self,proizvodjac):
        self.proizvodjac=proizvodjac
    def set_cijena(self,cijena):
        self._cijena=cijena
    def set_kolicina(self,kolicina):
        self._kolicina=kolicina
    def na_popustu(self,popust):
        self._cijena-=(self._cijena*float(popust[:-1])*0.01)#micemo % iz stringa i mnozimo sa 0.01
    def stampa(self):
        print(f"{self.naziv}-{self.proizvodjac},{self._cijena}")
    def __repr__(self):
        return f'{self.naziv}-{self.proizvodjac},{self._kolicina} kutija'
    

class Zaposleni:
    def __init__(self,ime,pozicija,datum_zaposlenja=[datetime.now().month,datetime.now().year]):
        self.ime=ime
        self.pozicija=pozicija
        if(self.pozicija=="Direktor"):
            self.__plata=2000
        elif(self.pozicija=="Menadzer"):
            self.__plata=850
        elif(self.pozicija=="Farmaceut"):
            self.__plata=700
        elif(self.pozicija=="Tehnicar"):
            self.__plata=450
        else:
            self.__plata=300
        self.datum_zaposlenja=datum_zaposlenja
        staz=datetime.now().year-datum_zaposlenja[1]
        staz=staz if (datetime.now().month-datum_zaposlenja[0]>=0) else staz-1 
        try:
            self.__plata+=self.__plata*(round(staz/5)*0.1)  #svakih 5 godina svaki zaposleni dobija povisicu za 10%
        except ZeroDivisionError as zero_division_error:
            self.__plata=self.__plata
    def get_ime(self):
        return self.ime
    def get_pozicija(self):
        return self.pozicija
    def get_datum_zaposlenja(self):
        return self.datum_zaposlenja
    def get_plata(self):
        return self.__plata
    def set_ime(self,ime):
        self.ime=ime
    def set_pozicija(self,pozicija):
        self.pozicija=pozicija
    def set_datum_zaposlenja(self,datum_zaposlenja):
        self.datum_zaposlenja=datum_zaposlenja
    def kazna(self,value):
        if isinstance(value, six.string_types): #korisnik moze da unese string 15% ili precizno iznos koji zeli da oduzme kao int ili float
            value=self.__plata*(int(value[:-1])*0.01)
        return self.__plata-value
    def __repr__(self):
        return f'{self.ime},{self.pozicija},{self.datum_zaposlenja[0]}/{self.datum_zaposlenja[1]},{self.__plata}'


class Kasa:
    def __init__(self,depozit,trenutno_stanje=0):
        self.depozit=depozit
        self.trenutno_stanje=depozit if trenutno_stanje<depozit else trenutno_stanje
    def get_depozit(self):
        return self.depozit
    def get_trenutno_stanje(self):
        return self.trenutno_stanje
    def set_depozit(self,depozit):
        self.depozit=depozit
    def prodato(self,lijek,kolicina):
        if(lijek.get_kolicina()>=kolicina):
            self.trenutno_stanje+=lijek.get_cijena()*kolicina
            lijek.set_kolicina(lijek.get_kolicina()-kolicina)
        else:
            print("Ovog artikla nema dovoljno na stanju za ovu prodaju")
    def profit(self):
        return self.trenutno_stanje-self.depozit



class Apoteka:
    def __init__(self, naziv,lokacija,stanje_ljekova,spisak_zaposlenih):
        self.naziv=naziv
        self.lokacija=lokacija
        self.stanje_ljekova=stanje_ljekova
        self.spisak_zaposlenih=spisak_zaposlenih
    def get_naziv(self):
        return self.naziv
    def get_lokacija(self):
        return self.lokacija
    def get_stanje_ljkova(self):
        return self.stanje_ljekova
    def get_spisak_zaposlenih(self):
        return self.spisak_zaposlenih
    def set_naziv(self,naziv):
        self.naziv=naziv
    def set_lokacija(self,lokacija):
        self.lokacija=lokacija
    def set_stanje_ljekova(self,stanje_ljekova):
        self.stanje_ljekova=stanje_ljekova
    def popis_manjak(self,realno_stanje_ljekova):
        spisak_manjak=[]
        manjak=0
        for lijek in self.stanje_ljekova:
            for lijek_popis in realno_stanje_ljekova:
                if(lijek.get_naziv()==lijek_popis.get_naziv() and lijek.get_kolicina()!=lijek_popis.get_kolicina()):
                    spisak_manjak.append(Lijek(lijek.get_naziv(),lijek.get_proizvodjac(),lijek.get_cijena(),lijek.get_kolicina()-lijek_popis.get_kolicina()))
                    manjak+=lijek.get_kolicina()-lijek_popis.get_kolicina()
        print("Ukupna vrijednost ljekova koji nedostaju je:",manjak,"e")
        return spisak_manjak
    def __repr__(self):
        return f'Naziv apoteke: {self.naziv}\nlokacija: {self.lokacija}\ntrenutno stanje ljekova: {self.stanje_ljekova}\nspisak zaposlenih: {self.spisak_zaposlenih}'
    def plate(self):
        plate=0
        for radnik in self.spisak_zaposlenih:
            plate+=radnik.get_plata()
        return plate






with open("ljekovi.json",encoding="utf8") as ljekovi:
    spisak_ljekova=json.load(ljekovi)
stanje_ljekova=[]
for lijek in spisak_ljekova:
    stanje_ljekova.append(Lijek(lijek["naziv"],lijek["proizvodjac"],lijek["cijena"],lijek["kolicina"]))

with open("zaposleni.json",encoding="utf8") as zap:
    spisak_zaposlenih=json.load(zap)
svi_zaposleni=[]
for zaposleni in spisak_zaposlenih:
    svi_zaposleni.append(Zaposleni(zaposleni["ime"],zaposleni["pozicija"],zaposleni["datum_zaposlenja"]))

with open("ljekovi_popis.json",encoding="utf8") as ljekovi_popis:
    spisak_ljekova_popis=json.load(ljekovi_popis)
stanje_ljekova_popis=[]
for lijek in spisak_ljekova_popis:
    stanje_ljekova_popis.append(Lijek(lijek["naziv"],lijek["proizvodjac"],lijek["cijena"],lijek["kolicina"]))

apoteka_1=Apoteka("Montefarm","Bl. Sv. Petra Cetinjskog",stanje_ljekova,svi_zaposleni)
print(apoteka_1)
print("Neophodan budzet za plate na mjesecnom nivou iznosi: ",apoteka_1.plate())
print("Nakon popisa utvrdjeno je da nedostaju ljekovi sa sledeceg spiska:",apoteka_1.popis_manjak(stanje_ljekova_popis))
