import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import util.generic as utl
from tkinter import filedialog
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib
import util.encoding_decoding as end_dec
from PIL import Image
import firebase_admin
from firebase_admin import credentials, firestore
from tkinter import messagebox
import os

class FormInsertionDesigner:   

    def __init__(self):
        self.ventana = tk.Tk()
        self.paciente = tk.StringVar()
        self.estudio = tk.StringVar()
        self.radiologo = tk.StringVar()
        self.especialista = tk.StringVar()
        self.fecha = tk.StringVar()
        self.imagen_seleccionada = None
        self.encrypted_text = None  # Variable para almacenar el texto cifrado

    def abrirImagen(self):
        ruta_imagen = filedialog.askopenfilename(filetypes=[("Imagen PNG", "*.png")])
        if ruta_imagen:
            self.imagen_seleccionada = ruta_imagen
            self.etiqueta_archivo_png.delete(0, tk.END)
            self.etiqueta_archivo_png.insert(0, os.path.basename(ruta_imagen))
            self.ventana.mainloop()
     
    def ocultar_mensaje(self, imagen_path, mensaje):
        imagen = Image.open(imagen_path)
        if imagen.mode != 'RGB':
            imagen = imagen.convert('RGB')
        ancho, alto = imagen.size
        mensaje_binario = ''.join(format(ord(c), '08b') for c in "marcada")+''.join(format(ord(caracter), '08b') for caracter in mensaje) + '1111111111111110'  # Marcador de fin de mensaje
        indice = 0
        for y in range(alto):
            for x in range(ancho):
                pixel = list(imagen.getpixel((x, y)))
                for i in range(3):  # Iterar sobre los tres canales de color RGB
                    if indice < len(mensaje_binario):
                        pixel[i] = pixel[i] & ~1 | int(mensaje_binario[indice])
                        indice += 1
                imagen.putpixel((x, y), tuple(pixel))
        nombre_archivo = 'RMI_marcada.png'
        if os.path.exists(nombre_archivo):
            nombre, extension = os.path.splitext(nombre_archivo)
            contador = 1
            nuevo_nombre = f"{nombre}_{contador}{extension}"
            while os.path.exists(nuevo_nombre):
                contador += 1
                nuevo_nombre = f"{nombre}_{contador}{extension}"
            archivo = nuevo_nombre
        else:
            archivo = nombre_archivo
        imagen.save(archivo)
    
    def borrarCampo(self):
        self.paciente.delete(0, tk.END)
        self.estudio.delete(0, tk.END)
        self.radiologo.delete(0, tk.END)
        self.especialista.delete(0, tk.END)
        self.fecha.delete(0, tk.END)

    def insertar(self):
         # OBTENCIÓN DE VALORES INGRESADOS EN CAJAS DE TEXTO
         datos = [self.paciente.get(), self.estudio.get(), self.radiologo.get(), self.especialista.get(), self.fecha.get()]
         # UNIR DATOS EN CADENA
         datos_concatenados = ",".join(datos)
         # MOSTRAR DATOS EN CONSOLA
         print("Datos del paciente:", datos_concatenados)

         # CIFRADO
         key = 'LlaveSuperSegura'  # Clave de cifrado (debería manejarse de forma segura)
         cipher = AES.new(key.encode(), AES.MODE_ECB)  # Modo ECB         
         # Asegurarse de que la longitud del texto sea un múltiplo de 16 bytes
         text = pad(datos_concatenados.encode('utf-8'), AES.block_size)
         self.encrypted_text = cipher.encrypt(text)  # Actualizar variable encrypted_text
         encrypted_text_str = base64.b64encode(self.encrypted_text).decode('utf-8')
         print("Texto Encriptado: ", encrypted_text_str+"###")

          # Generar IV
         iv = base64.b64encode(cipher.iv).decode('utf-8') if hasattr(cipher, 'iv') else None
         print("IV: ", iv)

         # OCULTAR MENSAJE EN LA IMAGEN SELECCIONADA
         if self.imagen_seleccionada:
             resultado_ocultar = self.ocultar_mensaje(self.imagen_seleccionada, encrypted_text_str)
             print(resultado_ocultar)
         else:
             print("No se ha seleccionado ninguna imagen.")

         #  MENSAJE DE MARCADO EXITOSO
         messagebox.showinfo("Marcación Exitosa", "La Imagen de Resonancia Magnética ha sido marcada exitósamente y guardada en el dispositivo")
         self.borrarCampo()

    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Cerrar sesión", "¿Quiere dejar de marcar imágenes?")
        if respuesta:
            messagebox.showinfo("Cerrar sesión", "Sesión cerrada.")
            self.ventana.destroy()



    def __init__(self):        
        self.ventana = tk.Toplevel()                             
        self.ventana.title('Insersión de la marca')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)    
        utl.centrar_ventana(self.ventana,800,550)
        self.ventana.lift()
        
        self.imagen_seleccionada = None        
        logo =utl.leer_imagen("./imagenes/rmi.png", (280, 350))

        #FRAME_LOGO
        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10,bg='#F87474')
        frame_logo.pack(side="left",expand=tk.NO,fill=tk.BOTH)
        label = tk.Label( frame_logo, image=logo,bg='#F87474')
        label.place(x=0,y=0,relwidth=1, relheight=1)
    
        #FRAME_FORM
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right",expand=tk.YES,fill=tk.BOTH)

        #FRAME_FORM_TOP
        frame_form_top = tk.Frame(frame_form,height = 50, bd=0, relief=tk.SOLID,bg='black')
        frame_form_top.pack(side="top",fill=tk.X)
        title = tk.Label(frame_form_top, text="Insertar Marca",font=('Times', 16), fg="#F87474",bg='#fcfcfc',pady=15)
        title.pack(expand=tk.YES,fill=tk.BOTH)
        
        #FRAME_FORM_TOP2
        frame_form_fill = tk.Frame(frame_form,height = 50,  bd=0, relief=tk.SOLID,bg='#fcfcfc')
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)       

        #ETIQUETA_CAJATEXTO
        etiqueta_paciente = tk.Label(frame_form_fill, text="Nombre del paciente", font=('Times', 14) ,fg="#000000",bg='#fcfcfc', anchor="w")
        etiqueta_paciente.pack(fill=tk.X, padx=20,pady=2)
        self.paciente = ttk.Entry(frame_form_fill, font=('Times', 10))
        self.paciente.insert(0, "ROMERO RUIZ RAFAEL")
        self.paciente.bind("<Button-1>", lambda e: self.paciente.delete(0, tk.END))
        self.paciente.pack(fill=tk.X, padx=20,pady=2)

        etiqueta_estudio = tk.Label(frame_form_fill, text="Nombre del estudio médico", font=('Times', 14),fg="#000000",bg='#fcfcfc' , anchor="w")
        etiqueta_estudio.pack(fill=tk.X, padx=20,pady=2)
        self.estudio = ttk.Entry(frame_form_fill, font=('Times', 10))
        self.estudio.insert(0, "RMI RODILLA IZQUIERDA 3 FLEX MRE")
        self.estudio.bind("<Button-1>", lambda e: self.estudio.delete(0, tk.END))
        self.estudio.pack(fill=tk.X, padx=20,pady=2)

        etiqueta_radiologo = tk.Label(frame_form_fill, text="Nombre del médico radiólogo", font=('Times', 14) ,fg="#000000",bg='#fcfcfc', anchor="w")
        etiqueta_radiologo.pack(fill=tk.X, padx=20,pady=2)
        self.radiologo = ttk.Entry(frame_form_fill, font=('Times', 10))
        self.radiologo.insert(0, "LUCIA LIMA LOPEZ")
        self.radiologo.bind("<Button-1>", lambda e: self.radiologo.delete(0, tk.END))
        self.radiologo.pack(fill=tk.X, padx=20,pady=2)
        
        etiqueta_especialista = tk.Label(frame_form_fill, text="Nombre del médico especialista", font=('Times', 14) ,fg="#000000",bg='#fcfcfc', anchor="w")
        etiqueta_especialista.pack(fill=tk.X, padx=20,pady=2)
        self.especialista = ttk.Entry(frame_form_fill, font=('Times', 10))
        self.especialista.insert(0, "MARIANO MENDEZ MORA")
        self.especialista.bind("<Button-1>", lambda e: self.especialista.delete(0, tk.END))
        self.especialista.pack(fill=tk.X, padx=20,pady=2)

        etiqueta_fecha = tk.Label(frame_form_fill, text="Fecha en la que se realizó el estudio", font=('Times', 14) ,fg="#000000",bg='#fcfcfc', anchor="w")
        etiqueta_fecha.pack(fill=tk.X, padx=20,pady=2)
        self.fecha = ttk.Entry(frame_form_fill, font=('Times', 10))
        self.fecha.insert(0, "28-06-2024")
        self.fecha.bind("<Button-1>", lambda e: self.fecha.delete(0, tk.END))
        self.fecha.pack(fill=tk.X, padx=20,pady=2)

        #BOTON1
        abrirImagen = tk.Button(frame_form_fill,text="Selecciona la RMI a marcar",font=('Times', 13),bg='#7f7f7f', bd=0,fg="#fff",command=self.abrirImagen)
        abrirImagen.pack(fill=tk.X, padx=20,pady=7)        
        abrirImagen.bind("<Return>", (lambda event: self.abrirImagen()))

        #CAJADETEXTO 
        self.etiqueta_archivo_png = tk.Entry(frame_form_fill, width=30)
        self.etiqueta_archivo_png.pack(fill=tk.X, padx=20,pady=7)

        #BOTON2
        insertar = tk.Button(frame_form_fill, text="Marcar", font=('Times', 13,BOLD), bg='#F87474', bd=0, fg="#fff", command=self.insertar)
        insertar.pack(fill=tk.X, padx=20, pady=7)
        insertar.bind("<Return>", (lambda event: self.insertar()))

        #BOTONBORRAR
        borrar = tk.Button(frame_form_fill, text="Borrar campos", font=('Times', 13,BOLD), bg='#F87474', bd=0, fg="#fff", command=self.borrarCampo)
        borrar.pack(fill=tk.X, padx=20, pady=7)
        borrar.bind("<Return>", (lambda event: self.borrarCampo()))

        #BOTONSESION
        cerrar_sesion = tk.Button(frame_form_fill, text="Cerrar sesión", font=('Times', 12,BOLD), bg='#F8F8FF', bd=0, fg="#000000", command=self.cerrar_sesion)
        cerrar_sesion.pack(fill=tk.X, padx=20, pady=7)
        cerrar_sesion.bind("<Return>", (lambda event: self.cerrar_sesion()))

        self.ventana.mainloop()



            

        
        
        
      