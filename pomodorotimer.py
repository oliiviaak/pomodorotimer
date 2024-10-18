import tkinter as tk
#import teema
from tkinter import messagebox
from ttkbootstrap import ttk, Style

class PomodoroTimer:
    def __init__(self):
        # Luo sovellusikkuna ja määritä sen koko ja otsikko. Sovelluksen pääikkunasta käytetään yleisesti nimeä root, jonka takia pääikkuna on asetettu tässäkin nimelle root.
        self.root = tk.Tk()
        self.root.geometry("300x250")  # Aseta ikkunan koko 300x250 pikseliä
        self.root.title("Pomodoro Timer")  # Ikkunan otsikko

        # Aseta teemaksi 'cyborg' käyttämällä ttkbootstrap. 
        self.style = Style(theme="cyborg") #Luodaan Style-olio
        self.style.theme_use() # Asetetaan teema aktiiviseksi koko sovellukselle
        
        #Koitettiin lisätä customoitua teemaa, mutta jostain syystä ohjelma ei suostu importoimaan teema.py tiedostoaaa pääohjelmaan ja tuo THEME attribuutti ei toimi
        #self.style = Style()
        #self.style.register_theme(teema.THEME)
        #self.style.theme_use('custom_theme')


        # Luo ajastimen näyttö ja lisää se ikkunaan
        self.timer_label = tk.Label(self.root, text="", font=("TkDefaultFont", 40))
        self.timer_label.pack(pady=20)  # Aseta ajastinnäytön ylä- ja alareunaan hieman tyhjää tilaa

        # Luo teksti, joka ohjeistaa syöttämään ajan minuutteina
        self.custom_time_label = ttk.Label(self.root, text="Enter custom time (minutes):")
        self.custom_time_label.pack(pady=5)

        # Luo syöttökenttä, johon käyttäjä voi kirjoittaa haluamansa ajan
        self.custom_time_entry = ttk.Entry(self.root)
        self.custom_time_entry.pack(pady=5)

        # Luo Start/Stop-painike ja lisää se ikkunaan
        # Käytetään harmaata väriä start-painikkeessa (bootstyle="secondary" tekee sen harmaaksi)
        self.start_stop_button = ttk.Button(self.root, text="Start", command=self.toggle_timer, bootstyle="secondary")
        self.start_stop_button.pack(pady=5)

        # Alustetaan tilamuuttujat: ajastin ei ole käynnissä, eikä se ole pysäytetty
        self.is_running = False
        self.is_paused = False
        self.work_time = 0  # Alustetaan työaika nollaksi

        # Liitä Enter-näppäin Start/Stop-painikkeeseen, jotta ajastimen voi aloittaa Enterillä
        self.root.bind('<Return>', lambda event: self.toggle_timer())

        # Käynnistä sovellusikkuna
        self.root.mainloop()

    def set_timer(self, work_time):
        # Aseta ajastinaika vain, jos ajastin ei ole käynnissä tai pysäytetty
        # Näin käyttäjän antama aika asetetaan vain alussa
        if not self.is_paused:
            self.work_time = work_time

    def toggle_timer(self):
        # Jos ajastin on käynnissä, pysäytetään se, muuten aloitetaan
        if self.is_running:
            self.stop_timer()
        else:
            self.start_custom_time_or_timer()

    def start_custom_time_or_timer(self):
        # Jos ajastin ei ole pysäytetty, haetaan uusi aika
        if not self.is_paused:
            custom_time = self.custom_time_entry.get()  # Haetaan käyttäjän antama aika syöttökentästä
            if custom_time:
                try:
                    custom_time_seconds = int(custom_time) * 60  # Muutetaan minuutit sekunneiksi
                    self.set_timer(custom_time_seconds)  # Aseta ajastimen aika
                except ValueError:
                    # Jos syötetty arvo ei ole numero, näytetään virheilmoitus
                    messagebox.showerror("Invalid input", "Please enter a valid number.")
                    return

        # Käynnistä ajastin
        self.is_running = True
        self.is_paused = False  # Ajastin ei ole enää pysäytetty
        # Vaihda Start-napin tekstiksi "Stop" ja tee siitä punainen
        self.start_stop_button.config(text="Stop", bootstyle="danger")
        self.update_timer()

    def stop_timer(self):
        # Pysäytä ajastin ja merkitse se pysäytetyksi
        self.is_running = False
        self.is_paused = True  # Ajastin on pysäytetty
        # Vaihda Stop-napin tekstiksi takaisin "Start" ja tee siitä harmaa
        self.start_stop_button.config(text="Start", bootstyle="secondary")

    def update_timer(self):
        # Tämä funktio päivittää ajastimen sekunnin välein
        if self.is_running:
            self.work_time -= 1  # Vähennetään yksi sekunti jäljellä olevasta ajasta
            if self.work_time <= 0:
                # Jos aika on loppu, pysäytetään ajastin ja näytetään ilmoitus
                self.stop_timer()
                messagebox.showinfo("Time's up!", "Your custom timer is complete!")
                return

            # Päivitetään ajastimen näyttö jäljellä olevalla ajalla
            minutes, seconds = divmod(self.work_time, 60)  # Muutetaan sekunnit minuuteiksi ja sekunneiksi
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))  # Näytetään aika muodossa MM:SS
            self.root.after(1000, self.update_timer)  # Kutsutaan itseään uudelleen sekunnin kuluttua

PomodoroTimer()
