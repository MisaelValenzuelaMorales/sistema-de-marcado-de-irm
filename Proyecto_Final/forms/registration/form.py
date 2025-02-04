from forms.registration.form_designer import FormRegisterDesigner
from forms.login.form_login_designer import FormLoginDesigner
from persistence.repository.auth_user_repository import AuthUserRepositroy
from tkinter import messagebox
import util.encoding_decoding as end_dec
import util.bd as bd
import tkinter as tk
import json
from collections import OrderedDict

class FormRegister(FormRegisterDesigner):
    
    def userRegister(self):
        FormRegister().mainloop()
    
    def registrar_Rad(self):
        if(self.isConfirmationPassword()):                    
            usuario = self.usuario.get()
            clave = self.confirmation.get()
            if not (self.isUserRegister(usuario)):
                clave = end_dec.encrypted(self.password.get())
                datos = {
                    'Usuario' : usuario,
                    'Clave' : clave,
                    'Perfil' : 'R'
                }
                bd.initializationBD().push(datos)
                self.ventana.destroy()                       

    def registrar_Esp(self):
        if(self.isConfirmationPassword()):                    
            usuario = self.usuario.get()
            clave = self.confirmation.get()
            if not (self.isUserRegister(usuario)):
                clave = end_dec.encrypted(self.password.get())
                datos = {
                    'Usuario' : usuario,
                    'Clave' : clave,
                    'Perfil' : 'E'
                }
                bd.initializationBD().push(datos)
                self.ventana.destroy()

    def isUserRegister(self, usuario):
        status: bool = False
        snapshot = bd.initializationBD().order_by_child('Usuario').equal_to(usuario).get()
        json_str = json.dumps(snapshot, indent=4)
        data = json.loads(json_str)
        if not data:
            messagebox.showinfo(message="Usuario registrado exitosamente", title="Mensaje")
        else:
            status = True
            messagebox.showerror(message="El usuario ya esta registrado", title="Mensaje")
            self.usuario.delete(0, tk.END)
            self.password.delete(0, tk.END)                
            self.confirmation.delete(0, tk.END)
        return status
    
    def isConfirmationPassword(self):
        status: bool = True
        if (self.password.get()=="") & (self.confirmation.get()==""):
            messagebox.showerror(message="La contraseña no puede estar vacía",title="Contraseña invalida")
        if(self.password.get() != self.confirmation.get()):
            status = False
            messagebox.showerror(
                message="La contraseña no coinciden por favor verifica el registro", title="Mensaje")
            self.password.delete(0, tk.END)                
            self.confirmation.delete(0, tk.END) 
        return status
    
    def inicio(self):
        respuesta = messagebox.askyesno("Regresar al inicio de sesión", "¿Quiere volver al inicio de sesión?")
        if respuesta:
            messagebox.showinfo("Inicio de sesión", "Regresará al menú principal")
            self.ventana.destroy()
    

