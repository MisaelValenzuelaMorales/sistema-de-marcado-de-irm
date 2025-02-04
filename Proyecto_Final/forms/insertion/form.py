from forms.insertion.form_designer import FormInsertionDesigner
from persistence.repository.auth_user_repository import AuthUserRepositroy
from persistence.model import Auth_User
from tkinter import messagebox
import util.encoding_decoding as end_dec
import tkinter as tk
from tkinter import filedialog

class FormInsertion(FormInsertionDesigner):

    def __init__(self):
        super().__init__()

    def abrirImagen(self):
        ruta_imagen = filedialog.askopenfilename(filetypes=[("Imagen PNG", "*.png")])
        if ruta_imagen:
            self.imagen_seleccionada = ruta_imagen
            self.etiqueta_archivo_png.delete(0, tk.END)
            self.etiqueta_archivo_png.insert(0, ruta_imagen.split('/')[-1])
            self.ventana.mainloop()