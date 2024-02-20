from pelicula import Pelicula
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql

def main():

    credentials = {
        "host": "localhost",
        "user": "dam_app",
        "password": "1234",
        "database": "pelis"
    }


    persistencia = Persistencia_pelicula_mysql(credentials)


    totes_les_pelicules = persistencia.totes()
    for pelicula in totes_les_pelicules:
        print(pelicula)

    pelicules1999 = persistencia.llegeix(1999)
    
    print("\n")
    
    for pelicula in pelicules1999:
        print(pelicula)


    pelicula = Pelicula("Nova peli",1999,8.8,97,persistencia)
    persistencia.desa(pelicula)

    


 

if __name__ == "__main__":
    main()






