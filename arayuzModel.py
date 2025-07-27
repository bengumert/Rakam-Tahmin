import tkinter as tk
from PIL import Image, ImageDraw, ImageOps  # pillowS
import numpy as np
from tensorflow.keras.models import load_model

# eğitilmiş model
model = load_model("mnist_model.h5")

class RakamTanimlayici:
    def __init__(self):
        # GUI için küütphane tk
        self.pencere = tk.Tk()
        self.pencere.title("Rakam Tanıma")

        self.tuval = tk.Canvas(self.pencere, width=200, height=200, bg='white')
        self.tuval.pack()

        self.gorsel = Image.new("L", (200, 200), 'white')
        # L IŞIK ŞİDDETİ
        self.cizim = ImageDraw.Draw(self.gorsel)

        self.tuval.bind('<B1-Motion>', self.ciz)

        tk.Button(self.pencere, text="Tahmin Et", command=self.tahmin_et).pack()
        tk.Button(self.pencere, text="Temizle", command=self.temizle).pack()

        self.sonuc_etiketi = tk.Label(self.pencere, text="", font=("Helvetica", 24))
        self.sonuc_etiketi.pack()

        self.pencere.mainloop()

    def ciz(self, olay):
        x1, y1 = (olay.x - 8), (olay.y - 8)
        x2, y2 = (olay.x + 8), (olay.y + 8)
        self.tuval.create_oval(x1, y1, x2, y2, fill='black')
        self.cizim.ellipse([x1, y1, x2, y2], fill='black')

    def temizle(self):
        self.tuval.delete("all")
        self.cizim.rectangle([0, 0, 200, 200], fill='white')
        self.sonuc_etiketi.config(text="")

    def tahmin_et(self):
        gorsel = self.gorsel.resize((28, 28))
        gorsel = ImageOps.invert(gorsel)
        gorsel = np.array(gorsel) / 255.0
        gorsel = gorsel.reshape(1, 28, 28, 1)
        tahmin = model.predict(gorsel)
        rakam = np.argmax(tahmin)
        self.sonuc_etiketi.config(text=f"Tahmin: {rakam}")

RakamTanimlayici()