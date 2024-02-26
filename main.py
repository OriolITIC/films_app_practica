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

    peliculas1999 = persistencia.llegeix(1999)
    print("\nPelículas del año 1999:")
    for pelicula in peliculas1999:
        print(pelicula)

    #nueva_pelicula = Pelicula("Nova peli2", 1999, 8.8, 97, persistencia)
    #persistencia.desa(nueva_pelicula)

    nueva_pelicula = Pelicula("Nova peli3",2001,8.9,99,persistencia,1704)
    print(persistencia.canvia(nueva_pelicula))
    persistencia.totes_pag(0)

    

if __name__ == "__main__":
    main()






