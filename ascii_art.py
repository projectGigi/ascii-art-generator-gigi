import os
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Caracteres japoneses para arte ASCII
ASCII_CHARS = "鬱鬼竜夢神愛炎零空月雨雪花竹山火水風"

# Ruta de fuente japonesa instalada
FONT_PATH = "/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf"  # Puedes cambiarla si usas otra

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.5)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join(ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixels)
    return characters

def convert_image_to_ascii(image_path, output_path, width=100):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")
        return

    image = resize_image(image, width)
    gray_image = grayify(image)

    ascii_str = pixels_to_ascii(gray_image)
    img_width = gray_image.width
    ascii_lines = [ascii_str[index:(index + img_width)] for index in range(0, len(ascii_str), img_width)]

    # Crear imagen con texto ASCII
    font_size = 12
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except OSError:
        print("No se pudo cargar la fuente japonesa. ¿Está instalada?")
        return

    line_height = font.getbbox("A")[3] + 2
    img_height = line_height * len(ascii_lines)
    img_width_pixels = font.getlength("A") * width

    img = Image.new("RGB", (int(img_width_pixels), img_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    for i, line in enumerate(ascii_lines):
        draw.text((0, i * line_height), line, font=font, fill=(0, 0, 0))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"✅ ASCII generado correctamente y guardado en: {output_path}")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Imagen", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        width = simpledialog.askinteger("Ancho del ASCII", "Ingresa el ancho del arte ASCII (ej: 100):", minvalue=10, maxvalue=500)
        if width:
            output_path = os.path.join("output", os.path.splitext(os.path.basename(file_path))[0] + "_ascii_jp.png")
            convert_image_to_ascii(file_path, output_path, width)
            messagebox.showinfo("Proceso completado", f"Imagen ASCII guardada en: {output_path}")

# GUI básica con tkinter
window = tk.Tk()
window.title("Generador de ASCII Japonés")
window.geometry("300x150")

label = tk.Label(window, text="Convierte imágenes a arte ASCII con kanji", wraplength=250)
label.pack(pady=10)

button = tk.Button(window, text="Seleccionar imagen", command=open_file)
button.pack(pady=10)

window.mainloop()
