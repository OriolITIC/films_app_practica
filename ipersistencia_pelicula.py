from abc import ABC, abstractclassmethod
from pelicula import Pelicula
from typing import List

# Aquest interfície proporciona un contracte que defineix els mètodes 
# que les classes de persistència de pel·lícules han d'implementar. 
#
# Serveix com a guia per a implementacions concretes on s'interactua 
# amb diferents bases de dades

class IPersistencia_pelicula(ABC):
    @abstractclassmethod
    def totes(self) -> List[Pelicula]:
        pass

    @abstractclassmethod
    def totes_pag(self,id: int) -> List[Pelicula]:
        pass
    
    @abstractclassmethod
    def desa(self, pelicula: Pelicula) -> Pelicula:
        pass

    @abstractclassmethod
    def canvia(self, pelicula: Pelicula) -> Pelicula:
        pass

    @abstractclassmethod
    def llegeix(self, any: int) -> Pelicula:
        pass