#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing import List
import psycopg

# La classe Persistencia_pelicula_postgresql
# proporciona funcionalitats per interactuar amb una base de dades PostgreSQL
class Persistencia_pelicula_postgresql(IPersistencia_pelicula):
    def __init__(self, credentials) -> None:
        self._credentials = credentials
        self._conn = psycopg.connect(
            host=credentials["host"],
            user=credentials["user"],
            password=credentials["password"],
            database=credentials["database"]
        )
        if not self.check_table():
            self.create_table()
    
    # Comprova si existeix la taula PELICULA a la base de dades.
    def check_table(self):
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM PELICULA;")
            cursor.fetchall()
        except psycopg.errors.UndefinedTable:
            return False
        return True
    
    # Retorna el nombre total de pel·lícules a la base de dades.
    def count(self) -> int:
        cursor = self._conn.cursor()
        query = "SELECT COUNT(*) FROM PELICULA;"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        return count
    
    # Retorna una llista de totes les pel·lícules de la base de dades.
    def totes(self) -> List[Pelicula]:
        cursor = self._conn.cursor()
        query = "SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA;"
        cursor.execute(query)
        registros = cursor.fetchall()
        resultado = []
        for registro in registros:
            pelicula = Pelicula(registro[1], registro[2], registro[3], registro[4], self, registro[0])
            resultado.append(pelicula)
        return resultado
    
    # Retorna una llista de pel·lícules de la base de dades a partir d'un id específic.   
    def totes_pag(self, id=None) -> List[Pelicula]:
        cursor = self._conn.cursor()
        query = "SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA WHERE id > %s LIMIT 10;"
        cursor.execute(query, (id,))
        registros = cursor.fetchall()
        resultado = []
        
        for registro in registros:
            pelicula = Pelicula(registro[1], registro[2], registro[3], registro[4], self, registro[0])
            resultado.append(pelicula)
        
        return resultado
    
    # Guarda una nova pel·lícula a la base de dades.
    def desa(self, pelicula: Pelicula) -> Pelicula:
        cursor = self._conn.cursor()
        query = "INSERT INTO PELICULA (titulo, anyo, puntuacion, votos) VALUES (%s, %s, %s, %s);"
        data = (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots)
        cursor.execute(query, data)
        self._conn.commit()
        cursor.close()
        return pelicula
    
    # Llegeix les pel·lícules d'un determinat any de la base de dades.
    def llegeix(self, any: int) -> List[Pelicula]:
        cursor = self._conn.cursor()
        query = "SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA WHERE anyo = %s;"
        cursor.execute(query, (any,))
        registros = cursor.fetchall()
        peliculas = []
        for registro in registros:
            pelicula = Pelicula(registro[1], registro[2], registro[3], registro[4], self, registro[0])
            peliculas.append(pelicula)
        return peliculas

    # Actualitza les dades d'una pel·lícula existent a la base de dades.
    def canvia(self, pelicula: Pelicula) -> Pelicula:
        cursor = self._conn.cursor()
        query = "UPDATE PELICULA SET titulo = %s, anyo = %s, puntuacion = %s, votos = %s WHERE id = %s;"
        data = (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots, pelicula.id)
        cursor.execute(query, data)
        self._conn.commit()
        cursor.close()
        return pelicula
