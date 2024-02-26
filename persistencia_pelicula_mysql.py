#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing import List
import mysql.connector
import logging

class Persistencia_pelicula_mysql(IPersistencia_pelicula):
    def __init__(self, credentials) -> None:
        self._credentials = credentials
        self._conn = mysql.connector.connect(
            host=credentials["host"],
            user=credentials["user"],
            password=credentials["password"],
            database=credentials["database"]
        )
        if not self.check_table():
            self.create_table()

    def check_table(self):
        try:
            cursor = self._conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM PELICULA;")
            cursor.reset()
        except mysql.connector.errors.ProgrammingError:
            return False
        return True
    
    def count(self) -> int:
        cursor = self._conn.cursor(buffered=True)
        query = "SELECT COUNT(*) FROM PELICULA;"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        return count
    
    def totes(self) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = "SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA;"
        cursor.execute(query)
        registros = cursor.fetchall()
        cursor.reset()
        resultado = []
        for registro in registros:
            pelicula = Pelicula(registro[1], registro[2], registro[3], registro[4], self, registro[0])
            resultado.append(pelicula)
        return resultado
    
    def totes_pag(self, id=None) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = "SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA WHERE id > %s LIMIT 10;"
        cursor.execute(query, (id,))
        registros = cursor.fetchall()
        cursor.reset()
        resultado = []
        for registro in registros:
            pelicula = Pelicula(registro[1], registro[2], registro[3], registro[4], self, registro[0])
            resultado.append(pelicula)
        print(resultado)
        return resultado
    
    def desa(self, pelicula: Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query = "INSERT INTO PELICULA (titulo, anyo, puntuacion, votos) VALUES (%s, %s, %s, %s);"
        data = (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots)
        cursor.execute(query, data)
        self._conn.commit()
        cursor.close()
        return pelicula
    
    def llegeix(self, any: int) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = "SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA WHERE anyo = %s;"
        cursor.execute(query, (any,))
        registros = cursor.fetchall()
        cursor.reset()
        peliculas = []
        for registro in registros:
            pelicula = Pelicula(registro[1], registro[2], registro[3], registro[4], self, registro[0])
            peliculas.append(pelicula)
        return peliculas

    
    def canvia(self, pelicula: Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query = "UPDATE PELICULA SET titulo = %s, anyo = %s, puntuacion = %s, votos = %s WHERE id = %s;"
        data = (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots, pelicula.id)
        cursor.execute(query, data)
        self._conn.commit()
        cursor.close()
        return pelicula

