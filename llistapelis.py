#!/bin/usr/python3

import json
from typing import List
from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql

# Llistapelis representa una llista de pel·lícules i ofereix funcions per llegir pel·lícules de la persistència de dades.

class Llistapelis():
    def __init__ (self, persistencia_pelicula: IPersistencia_pelicula) -> None:
        # Inicialitza una nova instància de Llistapelis.
        #   - persistencia_pelicula: Objecte de la classe que implementa la persistència de pel·lícules.
        # La funció inicialitza les propietats de la llista de pel·lícules, l'últim id de pel·lícula i la persistència de pel·lícules.
        self._pelicules = []  # Llista de pel·lícules.
        self._ult_id = 0  # Últim idç de pel·lícula.
        self._persistencia_pelicula = persistencia_pelicula  
        
    @property
    def pelicules(self) -> List[Pelicula]:
        return self._pelicules
    
    @property
    def ult_id(self) -> int:
        # Propietat que retorna l'últim id de pel·lícula.
        return self._ult_id

    @property
    def persistencia_pelicula(self) -> IPersistencia_pelicula:
        # Propietat que retorna la persistència de pel·lícules.
        return self._persistencia_pelicula
    
    def __repr__(self):
        return self.toJSON()
    
    def toJSON(self):
        pelicules_dict = []
        for pelicula in self._pelicules:
            pelicules_dict.append(json.loads(pelicula.toJSON()))
        self_dict = {
            "pelicules": pelicules_dict
            }   
        return json.dumps(self_dict)

    def llegeix_de_disc(self, id: int):
        # Llegeix pel·lícules de la persistència de dades a partir d'un id específic.
        #   - id: Id a partir del qual es vol llegir les pel·lícules.
        # La funció retorna una llista de pel·lícules llegides de la persistència de dades.
 
        # Utilitza la funció totes_pag de la persistència de pel·lícules per llegir les pel·lícules a partir del id especificat.
        peliculas = self._persistencia_pelicula.totes_pag(id)   
        
        # Si hi ha pel·lícules llegides, les afegeix a la llista de pel·lícules i actualitza l'últim id de pel·lícula.
        if peliculas:
            self._pelicules.extend(peliculas)
            self._ult_id = peliculas[-1].id 
        
        return peliculas



    

    
        
       


