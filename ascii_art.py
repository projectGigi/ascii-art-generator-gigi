import os
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, messagebox

ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii_color_image(input_path, output_path, new_width=100):
    try:
        image = Image.open(input_path).convert("RGB")
    except Exception as e:
        raise RuntimeError(f"Error al abrir la imagen: {e}")

    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.55)
    image = image.resize((new_width, new_height))

    grayscale = image.convert("L")
    pixels_brightness = list(grayscale.getdata())
    pixels_color = list(image.getdata())

    ascii_str = "".join([
        ASCII_CHARS[int(brightness / 255 * (len(ASCII_CHARS) - 1))]
        for brightness in pixels_brightness
    ])

    img_width = image.width
    img_height = image.height

    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        font = ImageFont.truetype(font_path, size=12)
    except Exception:
        font = ImageFont.load_default()

    bbox = font.getbbox("A")
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]

    img_out = Image.new("RGB", (char_width * img_width, char_height * img_height), color=(15, 15, 15))
    draw = ImageDraw.Draw(img_out)

    for i in range(img_height):
        for j in range(img_width):
            c = ascii_str[i * img_width + j]
            color = pixels_color[i * img_width + j]
            x = j * char_width
            y = i * char_height
            draw.text((x, y), c, fill=color, font=font)

    img_out.save(output_path)

def image_to_ascii_bw_image(input_path, output_path, new_width=100):
    try:
        image = Image.open(input_path).convert("L")
    except Exception as e:
        raise RuntimeError(f"Error al abrir la imagen: {e}")

    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.55)
    image = image.resize((new_width, new_height))

    pixels_brightness = list(image.getdata())

    ascii_str = "".join([
        ASCII_CHARS[int(brightness / 255 * (len(ASCII_CHARS) - 1))]
        for brightness in pixels_brightness
    ])

    img_width = image.width
    img_height = image.height

    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        font = ImageFont.truetype(font_path, size=12)
    except Exception:
        font = ImageFont.load_default()

    bbox = font.getbbox("A")
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]

    img_out = Image.new("L", (char_width * img_width, char_height * img_height), color=255)
    draw = ImageDraw.Draw(img_out)

    for i in range(img_height):
        line = ascii_str[i * img_width:(i + 1) * img_width]
        draw.text((0, i * char_height), line, fill=0, font=font)

    img_out.save(output_path)

class ASCIIArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador ASCII Oficial de Gigi")
        self.root.configure(bg="#121212")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        self.input_path = None
        self.output_dir = os.path.join(os.getcwd(), "output")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Estilos retro pixel
        btn_style = {"bg": "#282828", "fg": "#FFFFFF", "font": ("Courier New", 11), "activebackground": "#383838", "activeforeground": "#FFFFFF", "bd":0}
        label_style = {"bg": "#121212", "fg": "#AAAAAA", "font": ("Courier New", 10)}
        title_style = {"bg": "#121212", "fg": "#00FF00", "font": ("Courier New", 16, "bold")}

        # Widgets
        self.lbl_title = tk.Label(root, text="Generador ASCII Oficial de Gigi", **title_style)
        self.lbl_title.pack(pady=(15, 10))

        self.btn_select_img = tk.Button(root, text="Seleccionar Imagen", command=self.select_image, **btn_style)
        self.btn_select_img.pack(pady=5)

        self.lbl_img_path = tk.Label(root, text="Ninguna imagen seleccionada", **label_style)
        self.lbl_img_path.pack()

        self.btn_select_output = tk.Button(root, text="Seleccionar Carpeta Destino", command=self.select_output_dir, **btn_style)
        self.btn_select_output.pack(pady=5)

        self.lbl_output_path = tk.Label(root, text=f"Destino: {self.output_dir}", **label_style)
        self.lbl_output_path.pack()

        self.lbl_width = tk.Label(root, text="Ancho ASCII (caracteres):", **label_style)
        self.lbl_width.pack(pady=(10,0))

        self.width_var = tk.IntVar(value=100)
        self.scale_width = tk.Scale(root, from_=20, to=200, orient=tk.HORIZONTAL, variable=self.width_var,
                                    bg="#121212", fg="#00FF00", troughcolor="#383838",
                                    highlightthickness=0, bd=0, font=("Courier New", 9))
        self.scale_width.pack()

        # Opción color o blanco y negro
        self.color_var = tk.IntVar(value=1)  # 1=color, 0=bw
        frame_color = tk.Frame(root, bg="#121212")
        frame_color.pack(pady=10)

        self.rb_color = tk.Radiobutton(frame_color, text="Color", variable=self.color_var, value=1,
                                       bg="#121212", fg="#00FF00", selectcolor="#282828", font=("Courier New", 10))
        self.rb_bw = tk.Radiobutton(frame_color, text="Blanco y Negro", variable=self.color_var, value=0,
                                    bg="#121212", fg="#00FF00", selectcolor="#282828", font=("Courier New", 10))
        self.rb_color.pack(side=tk.LEFT, padx=15)
        self.rb_bw.pack(side=tk.LEFT, padx=15)

        self.btn_generate = tk.Button(root, text="Generar ASCII PNG", command=self.generate_ascii, **btn_style)
        self.btn_generate.pack(pady=15)

        self.btn_reset = tk.Button(root, text="Resetear Selección", command=self.reset_selection, **btn_style)
        self.btn_reset.pack()

        self.lbl_status = tk.Label(root, text="", **label_style)
        self.lbl_status.pack(pady=10)

    def select_image(self):
        filetypes = [("Imágenes", "*.jpg *.jpeg *.png *.bmp"), ("Todos los archivos", "*.*")]
        path = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=filetypes)
        if path:
            self.input_path = path
            self.lbl_img_path.config(text=f"Imagen seleccionada: {os.path.basename(path)}")
            self.lbl_status.config(text="")

    def select_output_dir(self):
        path = filedialog.askdirectory(title="Destino")
        if path:
            self.output_dir = path
            self.lbl_output_path.config(text=f"Destino: {self.output_dir}")
            self.lbl_status.config(text="")

    def generate_ascii(self):
        if not self.input_path:
            messagebox.showwarning("Advertencia", "Debe seleccionar una imagen primero.")
            return
        try:
            new_width = self.width_var.get()
            output_filename = f"{os.path.splitext(os.path.basename(self.input_path))[0]}"
            if self.color_var.get() == 1:
                output_filename += "_color.png"
                output_path = os.path.join(self.output_dir, output_filename)
                image_to_ascii_color_image(self.input_path, output_path, new_width=new_width)
            else:
                output_filename += "_bw.png"
                output_path = os.path.join(self.output_dir, output_filename)
                image_to_ascii_bw_image(self.input_path, output_path, new_width=new_width)

            self.lbl_status.config(text=f"✅ ASCII PNG generado: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.lbl_status.config(text="❌ Error al generar ASCII PNG")

    def reset_selection(self):
        self.input_path = None
        self.lbl_img_path.config(text="Ninguna imagen seleccionada")
        self.lbl_status.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = ASCIIArtApp(root)
    root.mainloop()

