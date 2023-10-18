import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Cargar el modelo previamente entrenado
modelo_cargado = load_model('modelo/modelo_digitos.keras')

class DibujarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dibuje un digito:")
        
        # Crear un lienzo
        self.lienzo = tk.Canvas(root, bg="white", width=280, height=280)
        self.lienzo.pack()
        
        # Crear un botón para guardar
        self.boton_consultar = tk.Button(root, text="Reconocer", command=self.consultar_ia)
        self.boton_consultar.pack()
        
        # Crear un botón para borrar el lienzo
        self.boton_borrar = tk.Button(root, text="Borrar Lienzo", command=self.borrar_lienzo)
        self.boton_borrar.pack()
        
        # Crear una etiqueta para mostrar la predicción
        self.etiqueta_prediccion = tk.Label(root, text="", font=("Helvetica", 20))
        self.etiqueta_prediccion.pack()
        
        # Configurar el pincel
        self.pincel = Image.new("L", (280, 280), "white")
        self.pincel_draw = ImageDraw.Draw(self.pincel)
        self.lienzo.bind("<B1-Motion>", self.dibujar)
        
    def dibujar(self, event):
        x, y = event.x, event.y
        radio = 5  # Tamaño del pincel
        self.lienzo.create_oval(x-radio, y-radio, x+radio, y+radio, fill="black")
        self.pincel_draw.ellipse([x-radio, y-radio, x+radio, y+radio], fill="black")
        
    def consultar_ia(self):
        file_path = "espacio1.png"  # Nombre de archivo fijo
        self.pincel.save(file_path)

        # Abre la imagen
        captura = Image.open("espacio1.png")

        # Invierte los colores de la imagen
        imagen_invertida = Image.new("L", captura.size)

        for x in range(captura.width):
            for y in range(captura.height):
                pixel_color = captura.getpixel((x, y))
                inverted_color = 255 - pixel_color
                imagen_invertida.putpixel((x, y), inverted_color)

        # Guarda la imagen invertida
        imagen_invertida.save("espacio1.png")

        # Cargar una imagen de prueba
        img_path = 'espacio1.png'
        img = image.load_img(img_path, target_size=(28, 28), color_mode="grayscale")
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Realizar la inferencia en la imagen de prueba
        resultado = modelo_cargado.predict(img_array)

        # Interpretar el resultado
        clase_predicha = np.argmax(resultado)
        
        os.remove('espacio1.png')

        # Mostrar la predicción en la etiqueta
        self.etiqueta_prediccion.config(text=f'El dígito reconocido es: {clase_predicha}')

    def borrar_lienzo(self):
        self.lienzo.delete("all")  # Borra todo en el lienzo
        self.pincel = Image.new("L", (280, 280), "white")
        self.pincel_draw = ImageDraw.Draw(self.pincel)
        self.etiqueta_prediccion.config(text="")  # Borra la predicción

if __name__ == "__main__":
    root = tk.Tk()
    app = DibujarApp(root)
    root.mainloop()
