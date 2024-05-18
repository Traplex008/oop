from abc import ABC, abstractmethod
import datetime


class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def leiras(self):
        pass


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar=10000):
        super().__init__(ar, szobaszam)

    def leiras(self):
        return f"Egyágyas szoba, ár: {self.ar} Ft, szobaszám: {self.szobaszam}"


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar=18000):
        super().__init__(ar, szobaszam)

    def leiras(self):
        return f"Kétagyas szoba, ár: {self.ar} Ft, szobaszám: {self.szobaszam}"


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum):
        if self._datum_ervenyes(datum):
            szoba = next((szoba for szoba in self.szobak if szoba.szobaszam == szobaszam), None)
            if szoba and not any(f for f in self.foglalasok if f.szobaszam == szobaszam and f.datum == datum):
                self.foglalasok.append(Foglalas(self, szobaszam, datum))
                return f"Foglalás megerősítve: {szoba.leiras()} dátumra: {datum}, ár: {szoba.ar} Ft"
            return "A szoba már foglalt erre a napra vagy nem létezik."
        return "A megadott dátum érvénytelen vagy múltbeli."

    def foglalas_lemondas(self, szobaszam, datum):
        for i, foglalas in enumerate(self.foglalasok):
            if foglalas.szobaszam == szobaszam and foglalas.datum == datum:
                del self.foglalasok[i]
                return "Foglalás törölve."
        return "Nincs ilyen foglalás."

    def foglalasok_listaja(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        return "\n".join(f"Foglalt: {f.szobaszam}, dátum: {f.datum}" for f in self.foglalasok)

    def _datum_ervenyes(self, datum):
        try:
            ev, honap, nap = map(int, datum.split('-'))
            datum_obj = datetime.date(ev, honap, nap)
            return datum_obj > datetime.date.today()
        except ValueError:
            return False


class Foglalas:
    def __init__(self, szalloda, szobaszam, datum):
        self.szalloda = szalloda
        self.szobaszam = szobaszam
        self.datum = datum


def felhasznaloi_interfesz():
    szalloda = Szalloda("Grand Hotel")
    szalloda.szoba_hozzaadas(EgyagyasSzoba(101))
    szalloda.szoba_hozzaadas(KetagyasSzoba(102))
    szalloda.szoba_hozzaadas(KetagyasSzoba(103))

    # Teszt foglalások hozzáadása
    teszt_datumok = ["2024-06-01", "2024-06-02", "2024-06-03", "2024-06-04", "2024-06-05"]
    for i in range(5):
        szalloda.foglalas(101 + i % 3, teszt_datumok[i])

    while True:
        print("\nVálassz egy műveletet:")
        print("1. Szoba foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        valasztas = input("Add meg a választott számot: ")

        if valasztas == "1":
            szobaszam = int(input("Add meg a szobaszámot: "))
            datum = input("Add meg a foglalás dátumát (ÉÉÉÉ-HH-NN formátumban): ")
            print(szalloda.foglalas(szobaszam, datum))
        elif valasztas == "2":
            szobaszam = int(input("Add meg a szobaszámot, amelyik foglalást le szeretnéd mondani: "))
            datum = input("Add meg a foglalás dátumát (ÉÉÉÉ-HH-NN formátumban): ")
            print(szalloda.foglalas_lemondas(szobaszam, datum))
        elif valasztas == "3":
            print("Jelenlegi foglalások:")
            print(szalloda.foglalasok_listaja())
        elif valasztas == "4":
            print("Kilépés a programból.")
            break
        else:
            print("Érvénytelen választás, próbáld újra.")


felhasznaloi_interfesz()
