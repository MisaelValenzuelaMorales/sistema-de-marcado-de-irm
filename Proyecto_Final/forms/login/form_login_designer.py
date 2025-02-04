import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import util.generic as utl

class FormLoginDesigner:
         
     def verificar(self):
        pass
     
     def userRegister(self):
        pass

     def __init__(self):        
        self.ventana = tk.Tk()                             
        self.ventana.title('Inicio de sesión')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)    
        utl.centrar_ventana(self.ventana,800,500)
        self.ventana.lift()
        
        logo =utl.leer_imagen("./imagenes/rmi.png", (280, 350))

        #FRAME_LOGO
        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10,bg='#17becf')
        frame_logo.pack(side="left",expand=tk.NO,fill=tk.BOTH)
        label = tk.Label( frame_logo, image=logo,bg='#17becf')
        label.place(x=0,y=0,relwidth=1, relheight=1)
    
        #FRAME_FORM
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right",expand=tk.YES,fill=tk.BOTH)

        #FRAME_FORM_TOP
        frame_form_top = tk.Frame(frame_form,height = 50, bd=0, relief=tk.SOLID,bg='black')
        frame_form_top.pack(side="top",fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesión",font=('Times', 27), fg="#17becf",bg='#fcfcfc',pady=50)
        title.pack(expand=tk.YES,fill=tk.BOTH)
        
        #FRAME_FORM_TOP2
        frame_form_fill = tk.Frame(frame_form,height = 50,  bd=0, relief=tk.SOLID,bg='#fcfcfc')
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)

        #ETIQUETA_CAJATEXTO
        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=('Times', 14) ,fg="#666a88",bg='#fcfcfc', anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20,pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=tk.X, padx=20,pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=('Times', 14),fg="#666a88",bg='#fcfcfc' , anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20,pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20,pady=10)
        self.password.config(show="*")

        #BOTON1
        inicio = tk.Button(frame_form_fill,text="Iniciar sesión",font=('Times', 15,BOLD),bg='#17becf', bd=0,fg="#fff",command=self.verificar)
        inicio.pack(fill=tk.X, padx=20,pady=20)        
        inicio.bind("<Return>", (lambda event: self.verificar()))

        #BOTON2
        inicio = tk.Button(frame_form_fill, text="Registrar usuario", font=('Times', 15), bg='#fcfcfc', bd=0, fg="#17becf", command=self.userRegister)
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind("<Return>", (lambda event: self.userRegister()))

         #BOTON3
        cerrar = tk.Button(frame_form_fill, text="Cerrar", font=('Times', 15), bg='#fcfcfc', bd=0, fg="#17becf", command=self.cerrar)
        cerrar.pack(fill=tk.X, padx=20, pady=20)
        cerrar.bind("<Return>", (lambda event: self.cerrar()))
        self.ventana.mainloop()