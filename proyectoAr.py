import csv
import json

Estudiantes_data=[]
Historial = []
def AltaEstudiante():
    nombre = str(input("Ingrese su nombre: "))
    carnet = int(input("Ingrese su carnet: "))
    carrera = str(input("Ingrese su carrera: "))
    edad = int(input("Ingrese su edad: "))

    estudiante = {
        "Nombre" : nombre,
        "Carnet" : carnet,
        "Carrera" : carrera,
        "Edad" : edad
    }
    Estudiantes_data.append(estudiante)
    Altas = {
        "Accion": "Alta",
        "Estudiante": estudiante
    }
    Historial.append(Altas)

def GuardarArchivos():
    with open("estudiantes.csv","w",newline="") as archivoCsv:
        fieldname = Estudiantes_data[0].keys()
        write = csv.DictWriter(archivoCsv, fieldnames=fieldname, delimiter=";")
        write.writeheader()
        write.writerows(Estudiantes_data)

    with open("estudiantes.json","w") as estuJ:
        json.dump(Estudiantes_data, estuJ,indent=4)

def BajarEstudiante():
    Acccion = {
        "Accion": "Baja",
        "Estudiante": Estudiantes_data.pop()
    }
    Historial.append(Acccion)


def CargarEstudiantes():
    with open("estudiantes.csv","r")as LectorCsv:
        lector = csv.DictReader(LectorCsv,delimiter=";")
        for elemento in lector:
            estu = {
                "Nombre": elemento["Nombre"],
                "Carnet": int(elemento["Carnet"]),
                "Carrera": elemento["Carrera"],
                "Edad": int(elemento["Edad"])
            }
            Estudiantes_data.append(estu)
            Accion = {
                "Accion": "Alta",
                "Estudiante": estu
            }
            Historial.append(Accion)

def Guardar_Historial():
    with open("historial.txt", "w") as archivoH:
        for h in Historial:
            archivoH.write(f"Accion {h['Accion']}, estudiante: {h['Estudiante']}")

def BusquedaSecuencia(id_Estudiante:int):
    encontrado = False
    while encontrado == False:
        with open("estudiantes.csv","r") as Buscardor:
            for linea in Buscardor:
                datos = linea.strip().split(";")
                if id_Estudiante == datos[1]:
                    print(f"Estudiante: {datos[0]} / {datos[2]} / {datos[3]}, encontrado")
                    encontrado=True
                    break
        
            if not encontrado:
                print(f"Estudiante con id: {id_Estudiante}, no existe")

#indice invertido
from collections import defaultdict
indice_invertido = defaultdict(list)

for indice, estudiante in enumerate(Estudiantes_data):
    texto_competo = f"{estudiante["Nombre"]} {estudiante["Carnet"]} {estudiante["Carrera"]} {estudiante["Edad"]}"
    for texto in texto_competo.split():
        if indice not in indice_invertido[texto]:
            indice_invertido[texto].append(indice)

def Busqueda_indice_invertido(busqueda:str):
    print(f"Buscar {busqueda} en el diccionario invertido: ")
    for f in indice_invertido[busqueda]:
        print("-", f)

indice_id = {i["Carnet"]: i for i in Estudiantes_data}
indice_Nombre = {n["Nombre"]: n for n in Estudiantes_data}
indice_Correo = {c["Correo"]: c for c in Estudiantes_data}

def BusquedaporId(id:int):
    print(f"Busqueda por Carnet: {indice_id[id]}")

def BusquedaporNombre(Nombre:str):
    print(f"Busqueda por Nombre: {indice_Nombre[Nombre]}")

def BusquedaporCorreo(Correo:str):
    print(f"Busqueda por Correo: {indice_Correo[Correo]}")

tamano = 50
tabla_hash = [None] * tamano

def funcionhash(clave):
    return hash(clave)%tamano

for Es in Estudiantes_data:
    hhid = funcionhash(Es["Carnet"])
    tabla_hash[hhid] = Es

def BusquedaHash(Carnet:int):
    hhid = funcionhash(Carnet)
    return tabla_hash[hhid]

import os
import shutil
from datetime import datetime

def Backup():
    origen = "estudiantes.json"
    destino = "backups"

    if not os.path.exists(destino):
        os.makedirs(destino)

    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_backup = f"backup_{fecha_hora}.json"

    ruta_backup = os.path.join(destino, nombre_backup)
    shutil.copy(origen, ruta_backup)

    print(f"Backup creado en: {ruta_backup}")

import stat
import time

def Metadatos():
    archivojson = "estudiantes.json"
    archivocsv = "estudiantes.csv"

    informacion_archivojson = os.stat(archivojson)
    print(f"Metadatos y permisos del archivo: {archivojson} \n")
    print("tamano",informacion_archivojson.st_size)
    print("creacion",time.ctime(informacion_archivojson.st_ctime))
    print("modificacion",time.ctime(informacion_archivojson.st_mtime))
    print("Ultimo acceso", time.ctime(informacion_archivojson.st_atime),"\n")

    permisosjson = informacion_archivojson.st_mode
    print("Lectura", bool(permisosjson & stat.S_IRUSR))
    print("Escritura", bool(permisosjson & stat.S_IWUSR))
    print("Ejecucion", bool(permisosjson&stat.S_IXUSR), "\n")

    informacion_archivocsv = os.stat(archivocsv)
    print(f"Metadatos y permisos del archivo: {archivocsv} \n")
    print("tamano",informacion_archivocsv.st_size)
    print("creacion",time.ctime(informacion_archivocsv.st_ctime))
    print("modificacion",time.ctime(informacion_archivocsv.st_mtime))
    print("Ultimo acceso", time.ctime(informacion_archivocsv.st_atime),"\n")

    permisoscsv = informacion_archivocsv.st_mode
    print("Lectura", bool(permisoscsv & stat.S_IRUSR))
    print("Escritura", bool(permisoscsv & stat.S_IWUSR))
    print("Ejecucion", bool(permisoscsv&stat.S_IXUSR), "\n")
    
CargarEstudiantes()
while True:
    EstudiantesCargados = False
    print("\n***** MENÚ PRINCIPAL *****")
    print("1. Alta de estudiante")
    print("2. Baja de estudiante")
    print("3. Buscar estudiante por ID")
    print("4. Buscar estudiante por nombre")
    print("5. Buscar estudiante por correo")
    print("6. Buscar en índice invertido")
    print("7. Realizar backup de datos")
    print("8. Mostrar metadatos de archivos")
    print("9. Salir")
    
    opc = input("Seleccione la opcion que desea realizar: ")

    if opc == "1":
        if len(Estudiantes_data) < 50:
            AltaEstudiante()
        else:
            print("Se a superado la cantidad maxima de estudiantes")
    elif opc == "2":
        if Estudiantes_data:
            BajarEstudiante()
        else:
            print("No hay ningun estudiante")
    elif opc == "3":
        if Estudiantes_data:
            carnet = int(input("Ingrese el carnet que desea buscar: "))
            print(f"\nBusqueda por indice multiple: {BusquedaporId(carnet)}")
            print(f"\nBusqueda por hash: {BusquedaHash(carnet)}")
            print(f"\nBusqueda por secuencia: {BusquedaSecuencia(carnet)}")
        else:
            print("No hay ningun estudiante")
    elif opc == "4":
        if Estudiantes_data:
            Nombre = input("Ingrese el nombre que desea buscar: ")
            print(f"\nBusqueda por indice multiple: {BusquedaporNombre(Nombre)}")
        else:
            print("No hay ningun estudiante")
    elif opc=="5":
        if Estudiantes_data:
            Correo = input("Ingrese el correo que desea buscar: ")
            print(f"\nBusqueda por indice multiple: {BusquedaporCorreo(Correo)}")
        else:
            print("No hay ningun estudiante")
    elif opc=="6":
        if Estudiantes_data:
            print("Busqueda por indice invertido\n")
            palabra = input("Ingrese la palabra que desea buscar: ")
            print(f"\nBusqueda por indice invertido: {Busqueda_indice_invertido(palabra)}")
        else:
            print("No hay ningun estudiante")
    elif opc=="7":
        print("Creando Backup...")
        GuardarArchivos()
        Guardar_Historial()
        Backup()
    elif opc=="8":
        Metadatos()
    elif opc=="9":
        print("saliendo...")
        break
    else:
        print("Error: elija una opcion valida")


