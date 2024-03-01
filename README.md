**1. Què fan els mètodes get_configuracio i get_persistencies?**

    El mètode get_configuracio llegeix un fitxer de configuració YAML i retorna un diccionari que conté la configuració obtinguda.

    El mètode get_persistencies rep un diccionari de configuració i retorna un altre diccionari que conté instàncies d'objectes necessaris per a la persistència de dades, com ara objectes de connexió a bases de dades.

**2. A procesa_opcio veureu instruccions com aquestes:**

    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis'])
    }

    # Què fa lambda? Com es podria reescriure el codi sense utilitzar lambda? Quina utilitat hi trobeu a utilitzar lambda?

    - Lambda és una funció anònima que es pot utilitzar per definir funcions en línia. Per exemple, en el codi donat es fa servir per a definir funcions senzilles dins d'un diccionari.
    
    Es podria reescriure el codi sense utilitzar lambda definint les funcions fora del diccionari:

    def fins_propera(ctx):
        mostra_lent("Fins la propera")

    def mostra_llista(ctx):
        mostra_llista(ctx['llistapelis'])

    return {
        "0": fins_propera,
        "1": mostra_llista
    }

**3. Penseu que s’ha desacoblat suficientment la lògica de negoci de la lògica d’aplicació? Raoneu la resposta i digueu si hi ha cap millora que es pugui fer.**

    En general, la lògica de negoci es troba suficientment desacoblat de la lògica de l'aplicació. No obstant, en el cas d'una aplicació més gran, seria important considerar millores en el maneig d'excepcions en els mètodes de persistència per augmentar la seva robustesa. A més, es podrien explorar patrons de disseny com el Singleton per optimitzar la gestió de les instàncies de connexió i millorar l'eficiència de l'aplicació.

