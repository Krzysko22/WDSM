import customtkinter as ctk
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ustawienia wyglądu
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MojaAplikacja:
    # Funkcja 1: __init__
    # Tworzy całe okno programu, boczne menu z polami i zakładki.
    def __init__(self):
        self.okno = ctk.CTk()
        self.okno.title("Symulator Stacji Bazowej - Zadanie 2")
        self.okno.geometry("1100x850")

        # PANEL BOCZNY
        self.bok = ctk.CTkFrame(self.okno, width=200)
        self.bok.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(self.bok, text="USTAWIENIA").pack(pady=5)

        # Pola do wpisywania
        ctk.CTkLabel(self.bok, text="Liczba kanalow (S):").pack()
        self.e1 = ctk.CTkEntry(self.bok);
        self.e1.insert(0, "8");
        self.e1.pack()

        ctk.CTkLabel(self.bok, text="Lambda (lambda):").pack()
        self.e2 = ctk.CTkEntry(self.bok);
        self.e2.insert(0, "0.4");
        self.e2.pack()

        ctk.CTkLabel(self.bok, text="Srednia (N):").pack()
        self.e3 = ctk.CTkEntry(self.bok);
        self.e3.insert(0, "60");
        self.e3.pack()

        ctk.CTkLabel(self.bok, text="Sigma (sig):").pack()
        self.e4 = ctk.CTkEntry(self.bok);
        self.e4.insert(0, "15");
        self.e4.pack()

        ctk.CTkLabel(self.bok, text="Min czas:").pack()
        self.e5 = ctk.CTkEntry(self.bok);
        self.e5.insert(0, "10");
        self.e5.pack()

        ctk.CTkLabel(self.bok, text="Maks czas:").pack()
        self.e6 = ctk.CTkEntry(self.bok);
        self.e6.insert(0, "300");
        self.e6.pack()

        ctk.CTkLabel(self.bok, text="Max kolejka:").pack()
        self.e7 = ctk.CTkEntry(self.bok);
        self.e7.insert(0, "10");
        self.e7.pack()

        ctk.CTkLabel(self.bok, text="Czas symulacji:").pack()
        self.e8 = ctk.CTkEntry(self.bok);
        self.e8.insert(0, "100");
        self.e8.pack()

        # Przycisk startu
        self.btn = ctk.CTkButton(self.bok, text="START", command=self.klik, fg_color="green")
        self.btn.pack(pady=20)

        # ZAKLADKI
        self.tabs = ctk.CTkTabview(self.okno)
        self.tabs.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.tab1 = self.tabs.add("Widok")
        self.tab2 = self.tabs.add("Wykresy")

        self.staty = ctk.CTkLabel(self.tab1, text="Czas: 0 | Obsluzone: 0", font=("Arial", 16))
        self.staty.pack()

        # Miejsce na rysowanie kanałów
        self.pole = ctk.CTkCanvas(self.tab1, bg="#1a1a1a", highlightthickness=0)
        self.pole.pack(fill="both", expand=True)

        self.dziala = False

    # Funkcja 2: klik
    # Odpala się po naciśnięciu przycisku START. Pobiera liczby z okienek i zeruje statystyki.
    def klik(self):
        # Pobieranie danych z pól Entry
        self.S = int(self.e1.get())
        self.lam = float(self.e2.get())
        self.N = float(self.e3.get())
        self.sig = float(self.e4.get())
        self.mn = float(self.e5.get())
        self.mx = float(self.e6.get())
        self.kq = int(self.e7.get())
        self.t_max = int(self.e8.get())

        # Przygotowanie list i zmiennych
        self.kanaly = [0] * self.S
        self.kolejka = []
        self.sekunda = 0
        self.obsluzone = 0
        self.l_rho = []
        self.l_q = []
        self.l_w = []
        self.wszystkie_czekania = []

        self.dziala = True
        self.tabs.set("Widok")
        self.symuluj()

    # Funkcja 3: symuluj
    # To jest "mózg" programu. Wykonuje 1 sekundę symulacji: sprawdza czy ktoś przyszedł, zajmuje kanały, obsługuje kolejkę i rysuje kolorowe prostokąty na ekranie.
    def symuluj(self):
        # Jeśli czas minął, przerwij i pokaż wykresy
        if not self.dziala or self.sekunda >= self.t_max:
            self.dziala = False
            self.koniec()
            return

        # Zmniejszamy czas trwania rozmów w zajętych kanałach
        for i in range(self.S):
            if self.kanaly[i] > 0:
                self.kanaly[i] -= 1

        if random.random() < self.lam:
            dlugosc = int(np.clip(np.random.normal(self.N, self.sig), self.mn, self.mx))

            wolny = -1
            for i in range(self.S):
                if self.kanaly[i] == 0:
                    wolny = i
                    break

            if wolny != -1:
                self.kanaly[wolny] = dlugosc
                self.obsluzone += 1
                self.wszystkie_czekania.append(0)
            else:
                if len(self.kolejka) < self.kq:
                    self.kolejka.append([dlugosc, self.sekunda])

        for i in range(self.S):
            if self.kanaly[i] == 0 and len(self.kolejka) > 0:
                osoba = self.kolejka.pop(0)
                self.kanaly[i] = osoba[0]
                self.obsluzone += 1
                self.wszystkie_czekania.append(self.sekunda - osoba[1])

        # Liczenie statystyk (Rho, Q, W)
        zajete = 0
        for k in self.kanaly:
            if k > 0: zajete += 1

        rho = zajete / self.S
        q_len = len(self.kolejka)
        w_sr = np.mean(self.wszystkie_czekania) if self.wszystkie_czekania else 0

        self.l_rho.append(rho)
        self.l_q.append(q_len)
        self.l_w.append(w_sr)

        # Rysowanie graficzne
        self.pole.delete("all")
        w = self.pole.winfo_width()
        for i in range(self.S):
            kolor = "red" if self.kanaly[i] > 0 else "green"
            y = 10 + i * 35
            self.pole.create_rectangle(50, y, w - 50, y + 30, fill=kolor)
            tekst = "Kanal " + str(i + 1) + ": " + (str(self.kanaly[i]) + "s" if self.kanaly[i] > 0 else "WOLNY")
            self.pole.create_text(w / 2, y + 15, text=tekst, fill="white")

        self.staty.configure(
            text="Sekunda: " + str(self.sekunda) + " | Obsluzone: " + str(self.obsluzone) + " | Kolejka: " + str(q_len))

        self.sekunda += 1
        self.okno.after(500, self.symuluj)

    # Funkcja koniec
    # Wywołuje się po zakończeniu czasu symulacji. Generuje 3 wymagane wykresy oraz zapisuje wszystkie dane do pliku tekstowego na dysku.
    def koniec(self):
        for widget in self.tab2.winfo_children():
            widget.destroy()

        # Tworzenie wykresów
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 8))
        fig.tight_layout(pad=3.0)

        ax1.plot(self.l_rho, color="blue")
        ax1.set_title("Intensywnosc (rho)")

        ax2.plot(self.l_q, color="red")
        ax2.set_title("Dlugosc kolejki (Q)")

        ax3.plot(self.l_w, color="green")
        ax3.set_title("Sredni czas czekania (W)")

        canvas = FigureCanvasTkAgg(fig, master=self.tab2)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.tabs.set("Wykresy")

        # Zapis do pliku tekstowego
        f = open("wyniki_zadanie2.txt", "w")
        f.write("PARAMETRY: S=" + str(self.S) + " L=" + str(self.lam) + " N=" + str(self.N) + "\n")
        f.write("Sekunda;Rho;Q;W\n")
        for i in range(len(self.l_rho)):
            f.write(str(i) + ";" + str(round(self.l_rho[i], 2)) + ";" + str(self.l_q[i]) + ";" + str(
                round(self.l_w[i], 2)) + "\n")
        f.close()
        print("Plik wyniki_zadanie2.txt gotowy!")

if __name__ == "__main__":
    app = MojaAplikacja()
    app.okno.mainloop()