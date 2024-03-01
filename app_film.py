#!/usr/bin/python3

import os, yaml, sys, time, json
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
from llistapelis import Llistapelis
import logging

from persistencia_pelicula_pgSQL import Persistencia_pelicula_postgresql

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
RUTA_FITXER_CONFIGURACIO_MYSQL = os.path.join(THIS_PATH, 'configuraciomySQL.yml')
RUTA_FITXER_CONFIGURACIO_POSTGRESQL = os.path.join(THIS_PATH, 'configuraciopgSQL.yml')

# Funció per obtenir la configuració des d'un fitxer YAML
def get_configuracio(ruta_fitxer_configuracio) -> dict:
    config = {}
    with open(ruta_fitxer_configuracio, 'r') as conf:
        config = yaml.safe_load(conf)
    return config

# Funció per obtenir la persistència de dades segons la configuració donada
def get_persistencia(conf: dict) -> dict:
    credenciales = {}
    motor = conf["base de dades"]["motor"].lower().strip()

    if motor == "mysql":
        credenciales = conf["base de dades"]
        return {
            'pelicula': Persistencia_pelicula_mysql(credenciales)
        }
    elif motor == "postgresql":
        credenciales = conf["base de dades"]
        return {
            'pelicula': Persistencia_pelicula_postgresql(credenciales)
        }
    else:
        return {
            'pelicula': None
        }

# Funció per mostrar un missatge lentament 
def mostra_lent(missatge, v=0.05):
    for c in missatge:
        print(c, end='')
        sys.stdout.flush()
        time.sleep(v)
    print()

# Funció per mostrar el text de benvinguda
def landing_text():
    os.system('clear')
    print("Benvingut a la app de pel·lícules")
    time.sleep(1)
    msg = "Desitjo que et sigui d'utilitat!"
    mostra_lent(msg)
    input("Prem la tecla 'Enter' per a continuar")
    os.system('clear')

# Funció per mostrar una llista de pel·lícules
def mostra_llista(llistapelicula):
    os.system('clear')
    mostra_lent(json.dumps(json.loads(llistapelicula.toJSON()), indent=4), v=0.01)

# Funció per mostrar les següents pel·lícules d'una llista
def mostra_seguents(llistapelicula):
    os.system('clear')
    mostra_lent(json.dumps(json.loads(llistapelicula.toJSON()), indent=4), v=0.01)

# Funció per seleccionar el motor de base de dades
def seleccionar_base_dades():
    while True:
        print("Quin motor de base de dades vols utilitzar?")
        print("1. MySQL")
        print("2. PostgreSQL")
        opcion = input("Selecciona el número corresponent a la teva elecció: ")
        if opcion == "1":
            print("Has seleccionat MySQL.")
            return "mysql"
        elif opcion == "2":
            print("Has seleccionat PostgreSQL.")
            return "postgresql"
        else:
            print("Opció invàlida. Si us plau, intenta-ho de nou.")

# Funció per mostrar el menú principal
def mostra_menu():
    print("0.- Surt de l'aplicació.")
    print("1.- Mostra les primeres 10 pel·lícules")

# Funció per mostrar el menú de les següents 10 pel·lícules
def mostra_menu_next10():
    print("0.- Surt de l'aplicació.")
    print("2.- Mostra les següents 10 pel·lícules")

# Funció per processar les opcions seleccionades
def procesa_opcio(context):
    return {
        "0": lambda ctx: mostra_lent("Fins la propera"),
        "1": lambda ctx: (mostra_llista(ctx['llistapelis']), mostra_menu_next10()),
        "2": lambda ctx: (mostra_seguents(ctx['llistapelis']) if ctx["llistapelis"] else print("No hi ha cap lista de películas carregada."), mostra_menu_next10())
    }.get(context["opcion"], lambda ctx: mostra_lent("opció incorrecta!!!"))(context)

# Funció per llegir les pel·lícules de la base de dades
def database_read(id:int, conf: dict):
    logging.basicConfig(filename='peliculas.log', encoding='utf-8', level=logging.DEBUG)
    persistencia = get_persistencia(conf)
    lista_peliculas = Llistapelis(persistencia['pelicula'])
    lista_peliculas.llegeix_de_disc(id)  
    return lista_peliculas

# Funció principal que gestiona el bucle principal de l'aplicació
def bucle_principal(contexto, conf: dict):
    opcion = None
    mostra_menu()
    while opcion != '0':
        opcion = input("Selecciona una opció: ")
        contexto["opcion"] = opcion
        
        if opcion == '1':
            id = 0
            contexto["llistapelis"] = database_read(id, conf)
      
        elif opcion == '2':
            if contexto["llistapelis"]:
                id += 10  
                contexto["llistapelis"] = database_read(id, conf)
            else:
                print("No hi ha cap llista de pelicules carregada.")
        elif opcion != '0':
            print("¡Opción incorrecta!")

        procesa_opcio(contexto)

# Funció principal de l'aplicació
def main():
    contexto = {
        "listapelis": None
    }
    landing_text()
    
    
    motor_bd = seleccionar_base_dades()
    if motor_bd == "mysql":
        configuracion = get_configuracio(RUTA_FITXER_CONFIGURACIO_MYSQL)
    elif motor_bd == "postgresql":
        configuracion = get_configuracio(RUTA_FITXER_CONFIGURACIO_POSTGRESQL)
    else:
        print("Motor de base de dades no compatible.")
        return
    
    bucle_principal(contexto, configuracion)

if __name__ == "__main__":
    main()
