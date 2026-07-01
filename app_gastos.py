import customtkinter as ctk
import json
from datetime import datetime
import os
from tkinter import messagebox
from tkinter import simpledialog

app = ctk.CTk()
app.title("Gestor de gastos")
app.geometry("800x600")

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_GASTOS = os.path.join(BASE,"gastos.json")


def cargar_gastos ():
  try:
   with open(ARCHIVO_GASTOS,"r") as archivo:
    datos = json.load(archivo)
    return datos["gastos"]
  except FileNotFoundError:
   return []
  except json.JSONDecodeError:
   return[]
   
gastos = cargar_gastos()
indice_edicion = None
 


def mostrar_registro():
    frame_menu.pack_forget()
    frame_registro.pack()

def mostrar_menu():
    frame_registro.pack_forget()
    frame_ver.pack_forget()
    frame_eliminar.pack_forget()
    frame_estadisticas.pack_forget()
    frame_menu.pack()

def guardar_gastos():
    global indice_edicion

    categoria = campo_categoria.get()
    monto = campo_monto.get()
    moneda = campo_moneda.get()
    descripcion = campo_desc.get()

    if  categoria == "Seleccione una categoria":
      messagebox.showerror("Error","Seleccione una categoria")
      return
    
    if not descripcion.strip():
      messagebox.showerror("Error","Ingrese una descripcion")
      return
    
    if moneda not in ["BOB","USD"]:
      messagebox.showerror("Error","Seleccione una moneda")
      return

    try:
      monto = float(monto)
    except ValueError:
      messagebox.showerror("Error","Monto Invalido")
      return
    
    if monto <= 0:
      messagebox.showerror("Error","El monto debe ser mayor a 0")
      return
    
    fecha = datetime.now().strftime("%d/%m/%Y")
    gasto = {
      "descripcion":descripcion,
      "monto":monto,
      "moneda":moneda,
      "categoria":categoria,
       "fecha":fecha
    }

    if indice_edicion is None:
      gastos.append(gasto)
      mensaje = "Gasto Registrado Exitosamente"
    else:
      gastos[indice_edicion] = gasto
      mensaje = "Gasto Actualizado Exitosamente"
      indice_edicion = None

    print("Guardando :",gasto)
    with open(ARCHIVO_GASTOS,"w") as archivo:
     json.dump({"gastos":gastos},archivo)
    messagebox.showinfo("Exito",mensaje)

    

    campo_categoria.set("Seleccione una categoria")
    campo_monto.delete(0,"end")
    campo_moneda.set("BOB")
    campo_desc.delete(0,"end")

    mostrar_menu()

def verificar_categoria (valor):

  if valor =="Otros":
    nueva_categoria = simpledialog.askstring("Nueva Categoria","Ingrese el nombre de la categoria :")

    if nueva_categoria:
     campo_categoria.set(nueva_categoria)

def mostrar_gastos():
  frame_menu.pack_forget()
  texto_ver.configure(state="normal")
  texto_ver.delete("1.0","end")
  if not gastos:
     texto_ver.insert("end","No hay gastos registrados\n")
  else:
      total_bob= 0
      total_usd= 0
      for i, gasto in enumerate(gastos , 1):
        linea = f"{i},{gasto['categoria']} |  {gasto['monto']} {gasto['moneda']} |  {gasto['descripcion']} |  {gasto['fecha']}\n"
        texto_ver.insert("end", linea)
  
        if gasto["moneda"] == "BOB":
         total_bob += gasto["monto"]
        else: 
         total_usd += gasto["monto"]

      texto_ver.insert("end", f"\nTOTAL BOB:{total_bob}\nTOTAL USD:{total_usd}\n")
  texto_ver.configure(state="disabled")
  frame_ver.pack()
  frame_editar.pack_forget()

def eliminar_gastos():
  frame_menu.pack_forget()
  texto_eliminar.configure(state="normal")
  texto_eliminar.delete("1.0","end")
  if not gastos:
     texto_eliminar.insert("end","No hay gastos registrados\n")
  else:
      total_bob= 0
      total_usd= 0
      for i, gasto in enumerate(gastos , 1):
        linea = f"{i},{gasto['categoria']} |  {gasto['monto']} {gasto['moneda']} |  {gasto['descripcion']} |  {gasto['fecha']}\n"
        texto_eliminar.insert("end", linea)
  
        if gasto["moneda"] == "BOB":
         total_bob += gasto["monto"]
        else: 
         total_usd += gasto["monto"]

      texto_eliminar.insert("end", f"\nTOTAL BOB:{total_bob}\nTOTAL USD:{total_usd}\n")
  texto_eliminar.configure(state="disabled")
  frame_eliminar.pack()

def confirmar_eliminar():
  try:
    eleccion = int(campo_eliminar.get().strip())

    if eleccion  < 1 or eleccion > len(gastos):
      raise IndexError
    respuesta = messagebox.askyesno("Confimar Eleccion","Estas seguro de Eliminar este gasto?")
    if not respuesta:
      return
    
    gastos.pop(eleccion -1)

    with open(ARCHIVO_GASTOS, "w") as archivo:
      json.dump({"gastos":gastos}, archivo)

    campo_eliminar.delete(0,"end")
    messagebox.showinfo("Exito","Gasto Eliminado Exitosamente")
    mostrar_menu()

  except(ValueError , IndexError):
    messagebox.showerror("Error","Numero Invalido")
  
def ver_edicion():
  frame_ver.pack_forget()
  frame_editar.pack()

def cargar_gastos_edit():
  global indice_edicion

  try:
    eleccion = int(campo_edit.get().strip())

    if eleccion < 1 or eleccion > len(gastos):
      raise IndexError
    indice_edicion = eleccion - 1
    gasto = gastos[indice_edicion] 

    
    campo_monto.delete(0,"end")
    campo_desc.delete(0,"end")

    campo_categoria.set(gasto["categoria"])
    campo_monto.insert(0,str(gasto["monto"]))
    campo_moneda.set(gasto["moneda"])
    campo_desc.insert(0,gasto["descripcion"])

    frame_editar.pack_forget()
    frame_registro.pack()
  except (ValueError , IndexError):
    messagebox.showerror("Error","Numero Invalido")

def mostrar_estadisticas():
  frame_menu.pack_forget ()

  texto_estadisticas.configure(state="normal")
  texto_estadisticas.delete("1.0","end")

  if not gastos:
    texto_estadisticas.insert("end","No hay gastos registrados.")
  else:
    estadisticas = {}

    total_bob = 0
    total_usd = 0

    for gasto in gastos:
      categoria = gasto["categoria"]
      monto = gasto["monto"]
      if categoria not in  estadisticas:
        estadisticas[categoria] = 0
      estadisticas[categoria] += monto
      if gasto["moneda"] == "BOB":
        total_bob += monto
      else:
        total_usd += monto
    texto_estadisticas.insert("end","📊 ESTADÍSTICAS\n\n","centrado")
    texto_estadisticas.insert("end",f"TOTAL BOB:{total_bob:.2f} BOB\n","centrado")
    texto_estadisticas.insert("end",f"TOTAL USD:{total_usd:.2f} USD\n\n","centrado")
    texto_estadisticas.insert("end","GASTOS POR CATEGORIA\n\n","centrado")

    for categoria, total in sorted(estadisticas.items(), key=lambda x: x[1],reverse=True):
      texto_estadisticas.insert("end",f"{categoria:<20}: {total:>10.2f}\n","centrado")
  texto_estadisticas.configure(state="disabled")
  frame_estadisticas.pack()


frame_menu = ctk.CTkFrame(app)
frame_menu.pack()

titulo = ctk.CTkLabel(frame_menu,text=" GESTOR DE GASTOS",font=("Arial",28,"bold"))
titulo.pack(pady=(30,40))

boton_1 = ctk.CTkButton(frame_menu, text="➕ REGISTRAR GASTO",width=250,height=45,command=mostrar_registro)
boton_1.pack(pady=10)

boton_2 = ctk.CTkButton(frame_menu, text="🗑 VER GASTOS",width=250,height=45,command=mostrar_gastos)
boton_2.pack(pady=10)

boton_3 = ctk.CTkButton(frame_menu, text="✏️ ELIMINAR GASTOS",width=250,height=45,command=eliminar_gastos)
boton_3.pack(pady=10)

boton_4 = ctk.CTkButton(frame_menu, text="📊 ESTADISTICAS",width=250,height=45,command=mostrar_estadisticas)
boton_4.pack(pady=10)


frame_registro = ctk.CTkFrame(app)

label = ctk.CTkLabel(frame_registro, text="REGISTRAR GASTO" )
label.pack(pady=10)

label_categoria = ctk.CTkLabel(frame_registro, text="CATEGORIA")
label_categoria.pack()

campo_categoria = ctk.CTkComboBox(frame_registro, values=["Comida","Transporte","Entretenimiento","Mascotas","Salud","Educacion","Otros"],width=200)
campo_categoria.set("Seleccione una categoria")
campo_categoria.pack(pady=5)

campo_categoria.configure(command=verificar_categoria)

frame_monto = ctk.CTkFrame(frame_registro)
frame_monto.pack(pady=5)

label_monto = ctk.CTkLabel(frame_monto, text="Monto")
label_monto.grid(row=0, column=0, padx=10)
campo_monto = ctk.CTkEntry(frame_monto, width=150)
campo_monto.grid(row=1, column=0, padx=10)

label_moneda = ctk.CTkLabel(frame_monto, text="Moneda")
label_moneda.grid(row=0, column=1, padx=10)

campo_moneda = ctk.CTkComboBox(frame_monto, values=["BOB","USD"], width=150)
campo_moneda.grid(row=1, column=1, padx=10)
campo_moneda.set("Elija una moneda :")

label_desc = ctk.CTkLabel(frame_registro, text="Descripcion")
label_desc.pack()
campo_desc = ctk.CTkEntry(frame_registro, width=400, placeholder_text="Descripcion del gasto")
campo_desc.pack(pady=5)


boton_guardar = ctk.CTkButton(frame_registro, text="GUARDAR", command=guardar_gastos)
boton_guardar.pack(pady=10)


boton_volver = ctk.CTkButton(frame_registro, text="VOLVER", command=mostrar_menu)
boton_volver.pack(pady=10)

frame_ver = ctk.CTkFrame(app)

texto_ver = ctk.CTkTextbox(frame_ver, width=600, height=400)
texto_ver.pack(pady=10)

boton_editar = ctk.CTkButton(frame_ver, text="EDITAR", command=ver_edicion)
boton_editar.pack(pady=10)

boton_volver = ctk.CTkButton(frame_ver, text="VOLVER", command=mostrar_menu)
boton_volver.pack(pady=10)

frame_editar = ctk.CTkFrame(app)

label_edit = ctk.CTkLabel(frame_editar, text="Numero del Gasto a Editar")
label_edit.pack(pady=10)
campo_edit = ctk.CTkEntry(frame_editar, placeholder_text="Elija un numero :")
campo_edit.pack(pady=10)

boton_cargar = ctk.CTkButton(frame_editar, text="CARGAR GASTOS", command=cargar_gastos_edit)
boton_cargar.pack(pady=5)

boton_volver_editar=ctk.CTkButton(frame_editar, text="VOLVER", command=mostrar_gastos)
boton_volver_editar.pack(pady=10)



frame_eliminar = ctk.CTkFrame(app)

texto_eliminar = ctk.CTkTextbox(frame_eliminar, width=600, height=400)
texto_eliminar.pack(pady=10)

campo_eliminar = ctk.CTkEntry(frame_eliminar, placeholder_text="Numero del gasto a eliminar")
campo_eliminar.pack(pady=10)

boton_eliminar=ctk.CTkButton(frame_eliminar, text="ELIMINAR GASTO", command=confirmar_eliminar)
boton_eliminar.pack(pady=10)

boton_volver = ctk.CTkButton(frame_eliminar, text="VOLVER", command=mostrar_menu)
boton_volver.pack(pady=5)


frame_estadisticas = ctk.CTkFrame(app)

texto_estadisticas = ctk.CTkTextbox(frame_estadisticas,width=600,height=400)
texto_estadisticas.pack(pady=10)
texto_estadisticas.tag_config("centrado",justify="center")

boton_volver = ctk.CTkButton(frame_estadisticas, text="VOLVER", command=mostrar_menu)
boton_volver.pack(pady=5)


app.mainloop()