import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import util.generic as utl
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import firebase_admin
from firebase_admin import credentials, firestore
from PIL import Image, ImageTk
from tkinter import Label

class FormExtracionDesigner:

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Extracción de Datos")
        self.imagen_seleccionada = None
        self.ventana.lift()
        self.encrypted_text = None  # Variable para almacenar el texto cifrado

        self.frame = ttk.Frame(self.ventana, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.etiqueta_archivo_png = ttk.Entry(self.frame, width=50)
        self.etiqueta_archivo_png.grid(row=0, column=0, padx=5, pady=5)

        self.boton_seleccionar = ttk.Button(self.frame, text="Seleccionar Imagen", command=self.seleccionar)
        self.boton_seleccionar.grid(row=0, column=1, padx=5, pady=5)

        self.boton_revelar = ttk.Button(self.frame, text="Revelar Información", command=self.revelar)
        self.boton_revelar.grid(row=1, column=0, columnspan=2, pady=10)


    def seleccionar(self):
        ruta_imagen = filedialog.askopenfilename(filetypes=[("Imagen PNG", "*.png")])
        imagen = Image.open(ruta_imagen)
        if ruta_imagen:
            self.imagen_seleccionada = Image.open(ruta_imagen)
            self.etiqueta_archivo_png.delete(0, tk.END)
            self.etiqueta_archivo_png.insert(0, ruta_imagen.split('/')[-1])
        imagen = self.imagen_seleccionada
        if imagen.mode != 'RGB':
            imagen = imagen.convert('RGB')
        ancho, alto = imagen.size
        mensaje_binario = ""
        for y in range(alto):
            for x in range(ancho):
                pixel = imagen.getpixel((x, y))
                for i in range(3):  # Iterar sobre los tres canales de color RGB
                    mensaje_binario += str(pixel[i] & 1)
        #Buscar el indicador de marcaje en la imagen
        marca_bin = ''.join(format(ord(c), '08b') for c in "marcada")
        marca = mensaje_binario.find(marca_bin)
        if marca != -1:
            tk.messagebox.showinfo("Información de la marca", "La imagen esta marcada, puede continuar")
            imagen_r = imagen.resize((140, 140))
            foto = ImageTk.PhotoImage(imagen_r)
            self.label = Label(self.ventana, image=foto)
            self.label.image = foto
            self.label.place(x=480, y=380)
        else:
            tk.messagebox.showinfo("Información de la marca", "La imagen NO esta marcada, seleccione otra para continuar")

    def extraer(self):
                imagen = self.imagen_seleccionada
                if imagen.mode != 'RGB':
                    imagen = imagen.convert('RGB')
                ancho, alto = imagen.size
                mensaje_binario = ""
                for y in range(alto):
                    for x in range(ancho):
                        pixel = imagen.getpixel((x, y))
                        for i in range(3):  # Iterar sobre los tres canales de color RGB
                            mensaje_binario += str(pixel[i] & 1)
                # Buscar el marcador de fin de mensaje
                fin_mensaje = mensaje_binario.find('1111111111111110')
                if fin_mensaje != -1:
                    mensaje_binario = mensaje_binario[56:fin_mensaje]
                caracteres = []
                for i in range(0, len(mensaje_binario), 8):
                    byte = mensaje_binario[i:i+8]
                    if len(byte) == 8:
                        caracteres.append(chr(int(byte, 2)))
                self.encrypted_text = ''.join(caracteres)
                self.encrypted_text_entry.insert(0, self.encrypted_text)  # Insertar el texto cifrado en la caja de texto
        
    def revelar(self):
                if self.encrypted_text:
                    self.encrypted_text = self.encrypted_text  # Actualizar variable encrypted_text
                decrypted_text = self.decrypt(self.encrypted_text)
                if decrypted_text is not None:
                    formatted_text = self.format_decrypted_text(decrypted_text)
                    tk.messagebox.showinfo("Información del paciente", formatted_text)
                else:
                    tk.messagebox.showwarning("Advertencia", "Error durante el descifrado.")

    def decrypt(self, encrypted_text):
        print("Encrypted text for decryption: ", encrypted_text)

        # Obtener la clave (debería manejarse de forma segura en un entorno real)
        key = 'LlaveSuperSegura'

        # Decodificar el texto cifrado de base64
        encrypted_text = base64.b64decode(encrypted_text)

        # Crear un objeto AES para descifrado en modo ECB
        cipher = AES.new(key.encode(), AES.MODE_ECB)

        try:
            # Descifrar el texto y deshacer el relleno
            decrypted_text = unpad(cipher.decrypt(encrypted_text), AES.block_size).decode('utf-8')
            return decrypted_text
        except Exception as e:
            print("Error durante el descifrado:", e)
            return None
        
    def format_decrypted_text(self, decrypted_text):
        # Separar el texto descifrado en partes usando la coma como delimitador
        datos = decrypted_text.split(',')

        # Crear el formato del mensaje
        formatted_text = (
            f"Nombre del paciente: {datos[0]}\n"
            f"Nombre del estudio: {datos[1]}\n"
            f"Nombre del médico radiólogo: {datos[2]}\n"
            f"Nombre del médico especialista: {datos[3]}\n"
            f"Fecha en la que se realizó el estudio: {datos[4]}"
        )
        return formatted_text
    
    def borrarCampo(self):
        self.etiqueta_archivo_png.delete(0, tk.END)
        self.encrypted_text_entry.delete(0, tk.END)
        self.label.destroy()


    def __init__(self):        
        self.ventana = tk.Toplevel()                             
        self.ventana.title('Extracción de la marca')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)    
        utl.centrar_ventana(self.ventana,800,550)
        
        logo =utl.leer_imagen("./imagenes/rmi.png", (280, 350))

        #FRAME_LOGO
        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10,bg='#3a7ff6')
        frame_logo.pack(side="left",expand=tk.NO,fill=tk.BOTH)
        label = tk.Label( frame_logo, image=logo,bg='#3a7ff6')
        label.place(x=0,y=0,relwidth=1, relheight=1)
    
        #FRAME_FORM
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right",expand=tk.YES,fill=tk.BOTH)

        #FRAME_FORM_TOP
        frame_form_top = tk.Frame(frame_form,height = 50, bd=0, relief=tk.SOLID,bg='black')
        frame_form_top.pack(side="top",fill=tk.X)
        title = tk.Label(frame_form_top, text="Extaer Marca",font=('Times', 20), fg="#3a7ff6",bg='#fcfcfc',pady=15)
        title.pack(expand=tk.NO,fill=tk.BOTH)
        
        #FRAME_FORM_TOP2
        frame_form_fill = tk.Frame(frame_form,height = 50,  bd=0, relief=tk.SOLID,bg='#fcfcfc')
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)       

        #BOTON1
        seleccionar = tk.Button(frame_form_fill,text="Selecciona la RMI a desmarcar",font=('Times', 14),bg='#7f7f7f', bd=0,fg="#fff",command=self.seleccionar)
        seleccionar.pack(fill=tk.X, padx=20,pady=10)        
        seleccionar.bind("<Return>", (lambda event: self.seleccionar()))

        #CAJADETEXTO 
        self.etiqueta_archivo_png = tk.Entry(frame_form_fill, width=30)
        self.etiqueta_archivo_png.pack(fill=tk.X, padx=20,pady=7)
        
        # BOTON2
        extraer = tk.Button(frame_form_fill, text="Extraer Marca", font=('Times', 14,BOLD), bg='#3a7ff6', bd=0, fg="#fff", command=self.extraer)
        extraer.pack(fill=tk.X, padx=20, pady=10)
        extraer.bind("<Return>", (lambda event: self.extraer()))

        # CAJA DE TEXTO PARA MOSTRAR EL MENSAJE CIFRADO
        self.encrypted_text_entry = tk.Entry(frame_form_fill, width=30)
        self.encrypted_text_entry.pack(fill=tk.X, padx=20, pady=7)   

        #BOTON3
        revelar = tk.Button(frame_form_fill, text="Revelar Marca", font=('Times', 14,BOLD), bg='#3a7ff6', bd=0, fg="#fff", command=self.revelar)
        revelar.pack(fill=tk.X, padx=20, pady=10)
        revelar.bind("<Return>", (lambda event: self.revelar()))

        #BOTONBORRAR
        borrar = tk.Button(frame_form_fill, text="Borrar campos", font=('Times', 14,BOLD), bg='#7f7f7f', bd=0, fg="#fff", command=self.borrarCampo)
        borrar.pack(fill=tk.X, padx=20, pady=10)
        borrar.bind("<Return>", (lambda event: self.borrarCampo()))

        #BOTONSESION
        cerrar_sesion = tk.Button(frame_form_fill, text="Cerrar sesión", font=('Times', 12,BOLD), bg='#F8F8FF', bd=0, fg="#000000", command=self.cerrar_sesion)
        cerrar_sesion.pack(fill=tk.X, padx=20, pady=3)
        cerrar_sesion.bind("<Return>", (lambda event: self.cerrar_sesion()))

        self.ventana.mainloop()

    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Cerrar sesión", "¿Quiere dejar de extraer marcas?")
        if respuesta:
            messagebox.showinfo("Cerrar sesión", "Sesión cerrada.")
            self.ventana.destroy()