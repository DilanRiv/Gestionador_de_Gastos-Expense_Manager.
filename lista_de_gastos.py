import json
from datetime import datetime
import os
import customtkinter as ctk 

app = ctk.CTk()
app.title("Gestor de Gastos")
app.geometry("600x400")


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
 
def registrar_gastos ():
 try:
  monto = float(input("Ingrese monto:\n"))
 except ValueError:
  print("Monto Invalido")
  return

 descripcion = input("Una descripcion:\n").strip()

 moneda = input("Moneda (BOB/USD):\n").strip().upper()

 print("Categorias:\n1.Comida\n2.Transporte\n3.Entretenimiento\n4.Salud\n5.Otro")
 categoria_op = input("Escoja una categoria\n").strip()

 categorias = {"1":"Comida","2":"Transporte","3":"Entretenimiento","4":"Salud"}
 if categoria_op =="5":
  categoria = input("Escribe una categoria:\n").strip()
 elif categoria_op in categorias:
  categoria = categorias[categoria_op]
 else:
  print("Opcion Invalida")
  return  

 fecha = datetime.now().strftime("%d/%m/%Y")

 gasto = {
  "descripcion":descripcion,
   "monto":monto,
   "moneda":moneda,
    "categoria":categoria,
    "fecha":fecha
 }
 gastos.append(gasto)

 with open(ARCHIVO_GASTOS,"w") as archivo:
  json.dump({"gastos":gastos},archivo)
 print("Gasto registrado exitosamente")

def mostrar_gastos (filtro=None):
  if not gastos:
   print("NO HAY GASTOS REGISTRADOS")
   return
  
  print("========= GASTOS REGISTRADOS ===========")
  total_bob= 0
  total_usd= 0

  for i, gasto in enumerate(gastos , 1):
   if filtro and gasto [filtro["campo"]].lower() != filtro["valor"].lower():
    continue
   print (str(i) + ". "+ gasto["categoria"] +"||"+ str(gasto["monto"]) +" "+ gasto["moneda"] +"||"+ gasto["descripcion"] +"||"+ gasto["fecha"] )

   if gasto["moneda"] == "BOB":
    total_bob += gasto["monto"]
   elif gasto["moneda"] == "USD":
    total_usd += gasto["monto"]

  print("========================================")
  print("TOTAL EN BOB:"+str(total_bob))
  print("TOTAL EN USD:"+str(total_usd))

def eliminar_gasto ():
 if not gastos:
  print("NO HAY GASTOS REGISTRADOS")
  return
 
 print("========= GASTOS REGISTRADOS ===========")
 for i, gasto in enumerate(gastos , 1):
  print (str(i) + ". "+ gasto["categoria"] +"||"+ str(gasto["monto"]) +" "+ gasto["moneda"] +"||"+ gasto["descripcion"] +"||"+ gasto["fecha"] )
 try :
  eleccion = int(input("ESCOJA UN GASTO (numero)\n").strip())
  print("========================================")
  gasto_ellegido = gastos[eleccion -1]

 except (ValueError , IndexError):
  print("Opcion Invalida")
  return

 confirmar = input("Esta seguro de eliminar este gasto?\n" + gasto_ellegido["descripcion"] +  " (si/no):\n").strip().lower()  

 if confirmar == "si":
  gastos.pop(eleccion - 1)
  with open(ARCHIVO_GASTOS, "w") as archivo:
   json.dump({"gastos":gastos},archivo)
  print("========================================")
  print("GASTO ELIMNADO")
 else:
  print ("Operacion Cancelada")
 
def buscar_gastos ():
 print("1. Por categoria\n 2. Por moneda\n3. Volver")
 opcion = input("Elegì: ").strip()

 if opcion == "1":
  categoria = input("Categoria : ").strip()
  mostrar_gastos({"campo":"categoria","valor": categoria})
 elif opcion == "2":
  moneda = input("Moneda (BOB/USD):").strip().upper()
  mostrar_gastos({"campo":"moneda","valor": moneda})
 elif opcion == "3":
  return






while True :

 opciones = input("Bienvenido a gestor de gastos\n1.Ingresar gastos\n2.Mostrar gastos\n3.Eliminar gasto\n4.Buscar Gastos\n5.SALIR\n ").strip().lower()
 if opciones =="1":
  
  registrar_gastos ()

 elif opciones =="2":

  mostrar_gastos ()

 elif opciones =="3":

  eliminar_gasto ()

 elif opciones =="4":

  buscar_gastos ()

 elif opciones =="5":

  print("HASTA LUEGO")
  break
 else:
  print("Opcion invalida")
  

app.mainloop()