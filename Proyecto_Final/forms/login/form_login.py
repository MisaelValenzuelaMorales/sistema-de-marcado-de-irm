import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.generic as utl
import util.bd as bd
from forms.login.form_login_designer import FormLoginDesigner
from persistence.repository.auth_user_repository import AuthUserRepositroy
from persistence.model import Auth_User
import util.encoding_decoding as end_dec
from forms.registration.form import FormRegister
import json
from collections import OrderedDict
from forms.insertion.form import FormInsertion
from forms.extraction.form import FormExtraction

class FormLogin(FormLoginDesigner):
        
        def radiologo(self):
            FormInsertion().mainloop()

        def especialista(self):
            FormExtraction().mainloop()
                    
        def userRegister(self):
            FormRegister().mainloop()     

        def cerrar(self):
            self.ventana.destroy()      
        
        def verificar(self):
            usuario = self.usuario.get()
            if(self.isUser(usuario)):
                self.isPassword(self.password.get(), usuario)
            
        def isUser(self, usuario):
            status: bool = True
            snapshot = bd.initializationBD().order_by_child('Usuario').equal_to(usuario).get()
            json_str = json.dumps(snapshot, indent=4)
            data = json.loads(json_str)
            if not data:
                status = False
                messagebox.showerror(
                    message="El usuario no existe, favor de registrarse", title="Mensaje",parent=self.ventana)
            return status

        def isPassword(self, password, usuario):
            snapshot = bd.initializationBD().order_by_child('Usuario').equal_to(usuario).get()
            json_str = json.dumps(snapshot, indent=4)
            data = json.loads(json_str)
            for clave, info in data.items():
                clave = info.get("Clave", "Clave no encontrada")
            for perfil, info in data.items():
                perfil = info.get("Perfil", "Perfil no encontrado")
            b_password = end_dec.decrypt(clave)
            if(password == b_password):
                if perfil == "R":
                    self.usuario.delete(0, tk.END)
                    self.password.delete(0, tk.END)
                    self.radiologo()
                elif perfil == "E":
                    self.usuario.delete(0, tk.END)
                    self.password.delete(0, tk.END)
                    self.especialista()
            else:
                messagebox.showerror(
                    message="La contraseña no es correcta", title="Mensaje")
     