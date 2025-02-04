import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import util.generic as utl


class FormRegisterDesigner():

    def register():
        pass

    def __init__(self):
        
        self.ventana = tk.Toplevel()
        self.ventana.title('Resgitro de usuario')        
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)
        utl.centrar_ventana(self.ventana, 800, 500)
        self.ventana.lift()

        logo = utl.leer_imagen("./imagenes/rmi.png", (215, 300))        

        #FRAME_LOGO
        frame_logo = tk.Frame(self.ventana, bd=0, width=200, relief=tk.SOLID, padx=10, pady=10, bg='#F0E68C')
        frame_logo.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg='#F0E68C')
        label.place(x=0, y=0, relwidth=1, relheight=1)

        #FRAME_FORM
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)
        
        #FRAME_FORM_TOP
        frame_form_top = tk.Frame(frame_form, height=30, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Registro de usuario", font=('Times', 27), fg="#F0E68C", bg='#fcfcfc', pady=30)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        
        #FRAME_FORM_TOP2
        frame_form_fill = tk.Frame(frame_form, height=50,  bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        #ETIQUETA_CAJATEXTO
        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=1)
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=4)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=1)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20, pady=4)
        self.password.config(show="*")
        
        etiqueta_confirmation = tk.Label(frame_form_fill, text="Confirmación", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_confirmation.pack(fill=tk.X, padx=20, pady=1)
        self.confirmation = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.confirmation.pack(fill=tk.X, padx=20, pady=4)
        self.confirmation.config(show="*")

        #SELECCIONAR_PERFIL
        etiqueta_perfil = tk.Label(frame_form_fill, text="Seleccione su perfil:",font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_perfil.pack(fill=tk.X, padx=20, pady=6)
        #BOTON1
        radiologo = tk.Button(frame_form_fill,text="Médico Radiólogo",font=('Times', 15,BOLD),bg='#F87474', bd=0,fg="#fff", command=self.registrar_Rad)
        radiologo.pack(fill=tk.X, padx=20,pady=7)
        radiologo.bind("<Return>", (lambda event: self.registrar_Rad()))     

        #BOTON2
        especialista = tk.Button(frame_form_fill,text="Médico Especialista",font=('Times', 15,BOLD),bg='#3a7ff6', bd=0,fg="#fff", command=self.registrar_Esp)
        especialista.pack(fill=tk.X, padx=20,pady=7) 
        especialista.bind("<Return>", (lambda event: self.registrar_Esp()))

        #BOTON3
        regresar_inicio = tk.Button(frame_form_fill, text="Volver al inicio", font=('Times', 15), bg='#F8F8FF', bd=0, fg="#000000", command=self.inicio)
        regresar_inicio.pack(fill=tk.X, padx=20, pady=7)
        regresar_inicio.bind("<Return>", (lambda event: self.inicio()))
        
        self.ventana.mainloop()
