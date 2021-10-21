"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso  ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
import time
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar cronológicamente los artistas")
    print("3- Listar cronológicamente las adquisiciones")
    print("4- Clasificar las obras de un artista por técnica")
    print("5- Clasificar las obras por nacionalidad de sus creadores")
    print("6- Transportar obras de un departamento")
    print("7- Proponer una nueva exposición en el museo")
    print("8- Listar obras por su nacionalidad")

    print("0- Salir")

def initCatalog():
    """
    Inicializa el catálogo de obras y artistas
    Returns: el catálogo

    """
    return controller.initCatalog()

def loadData(catalog):
    """
    Carga los datos.
    Args:
        catalog: el catálogo.

    """

    controller.loadData(catalog)

def getArtistsByDates(catalog,year1,year2):
    """
    Selecciona una porción de la lista de artistas que cumplen con el rango de fechas
    Args:
        catalog: Catálogo de artistas y obras
        year1: Año inicial del rango
        year2: Año final del rango

    Returns: Lista de los artistas que cumplen
    """

    return controller.getArtistsByDates(catalog, year1, year2)

def getArtworksByDates(catalog,date1,date2):
    """
    Selecciona una porción de la lista de obras de arte que cumplen con el rango de fechas
    Args:
        catalog: Catálogo de artistas y obras
        date1: Fecha inicial del rango
        date2: Fecha final del rango

    Returns: Lista de las obras que cumplen

    """
    return controller.getArtworksByDates(catalog,date1,date2)

def countPurchasedArtworks(artworks):
    """
    Cuenta las obras adquiridas mediante compra
    Args:
       artworks: Lista de obras de arte

    Returns: Total de obras

    """
    return controller.countPurchasedArtworks(artworks)


def classifyArtworksByTechnique(catalog,artistName):
    return controller.classifyArtworksByTechnique(catalog,artistName)

def classifyArtworksByNationality(catalog):
    return controller.classifyArtworksByNationality(catalog)

def getArtworksByDepartment(catalog,department):
    return controller.getArtworksByDepartment(catalog,department)

def getArtworksByNationality(catalog, nationality):
    return controller.getArtworksByNationality(catalog, nationality)

def estimateCosts(artworks):
    return controller.estimateCosts(artworks)

def pickFiveOldestArtworks(artworks):
    return controller.pickFiveOldestArtworks(artworks)

def pickFiveMostExpensive(artworks):
    return controller.pickFiveMostExpensive(artworks)

def getArtworksByYearAndArea(catalog,year1,year2,areaMax):
    return controller.getArtworksByYearAndArea(catalog,year1,year2,areaMax)

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1: # Carga de datos
        start_time = time.process_time()
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        # Imprimimos las cantidades de artistas y obras
        sizeArtists = lt.size(catalog['artists'])
        sizeArtworks = lt.size(catalog['artworks'])
        print('Artistas cargados: ' + str(sizeArtists))
        print('Obras cargadas: ' + str(sizeArtworks))

        #Imprimimos los últimos tres artistas
        print()
        print('Últimos tres artistas: ')
        print('- ' + str(lt.getElement(catalog['artists'], sizeArtists - 2)['DisplayName']))
        print('- ' + str(lt.getElement(catalog['artists'], sizeArtists - 1)['DisplayName']))
        print('- ' + str(lt.getElement(catalog['artists'], sizeArtists)['DisplayName']))

        #Imprimimos las últimas tres obras
        print()
        print('Últimas tres obras: ')
        print('- ' + str(lt.getElement(catalog['artworks'], sizeArtworks - 2)['Title']))
        print('- ' + str(lt.getElement(catalog['artworks'], sizeArtworks - 1)['Title']))
        print('- ' + str(lt.getElement(catalog['artworks'], sizeArtworks)['Title']))

        print() # Este se usa para dar un salto de línea
        stop_time = time.process_time()
        etms = (stop_time - start_time)*1000
        print('El tiempo de ejecucion es ' + str(etms) + 'ms')
        print()

    elif int(inputs[0]) == 2: # Requerimiento 1
        year1 = int(input('Ingrese el año inicial para la búsqueda: '))
        year2 = int(input('Ingrese el año final para la búsqueda: '))
        print()

        st = time.process_time()
        selectedArtists = getArtistsByDates(catalog, year1, year2)
        selectedSize = lt.size(selectedArtists)
        print(f'Hay {selectedSize} artistas nacidos entre {year1} y {year2}')
        print()
        print('Los primeros y últimos tres artistas en el rango son...')

        # Imprimimos el encabezado de la tabla
        print('Nombre\t\tAño de nacimiento\t\tAño de fallecimiento\t\tNationalidad\t\tGénero')
        # Imprimimos los tres primeros y los tres últimos
        firstAndLast = [1,2,3,selectedSize-2,selectedSize-1,selectedSize]
        for i in firstAndLast:
            artist = lt.getElement(selectedArtists, i)
            displayName = artist['DisplayName']
            beginDate = artist['BeginDate']
            endDate = artist['EndDate']
            nationality = artist['Nationality']
            gender = artist['Gender']
            print(f'{displayName}\t\t{beginDate}\t\t{endDate}\t\t{nationality}\t\t{gender}')
        spt = time.process_time()
        etms = (spt - st)*1000
        print('El tiempo de ejecucion es ' + str(etms) + 'ms')
        print()


    elif int(inputs[0]) == 3: # Requerimiento 2
        date1 = input('Ingrese la fecha inicial para la búsqueda (AAAA-MM-DD): ')
        date2 = input('Ingrese la fecha final para la búsqueda (AAAA-MM-DD): ')
        print()
        st = time.process_time()
        selectedArtworks = getArtworksByDates(catalog,date1,date2)
        selectedSize = lt.size(selectedArtworks)
        purchasedSize = countPurchasedArtworks(selectedArtworks)
        print(f'Se adquirieron {selectedSize} piezas únicas entre {date1} y {date2}.')
        print(f'De ellas, se compraron {purchasedSize}.')
        print()

        print('Las primeras y últimas tres obras de arte en el rango son...')

        # Imprimimos el encabezado
        print('Título\t\tArtista(s)\t\tFecha\t\tMedio\t\tDimensiones')
        # Imprimimos los tres primeros y los tres últimos
        firstAndLast = [1, 2, 3, selectedSize - 2, selectedSize - 1, selectedSize]
        for i in firstAndLast:
            artwork = lt.getElement(selectedArtworks,i)
            title = artwork['Title']
            constituentID = artwork['ConstituentID'][1:-1].split(',')
            artists = []
            for id in constituentID:
                for artist in catalog['artists']['elements']:
                    if artist['ConstituentID'] == id:
                        artists.append(artist['DisplayName'])
                        break

            artists = ', '.join(artists)
            date = artwork['Date']
            medium = artwork['Medium']
            dimensions = artwork['Dimensions']
            print(f'{title}\t\t{artists}\t\t{date}\t\t{medium}\t\t{dimensions}')

        print()
        spt = time.process_time()
        etms = (spt - st)*1000
        print('El tiempo de ejecucion es ' + str(etms) + 'ms')
        print()


    elif int(inputs[0]) == 4: # Requerimiento 3
        artistName = input('Ingrese el nombre del artista: ')
        st = time.process_time()
        techniquesMap = classifyArtworksByTechnique(catalog,artistName)
        techniques = mp.keySet(techniquesMap)
        artworksSubSets = mp.valueSet(techniquesMap)

        sizeArtworks = 0
        sizeTechniques = mp.size(techniquesMap)
        maxValue = 0  # Valor utilizado para comparar la cantidad de obras por técnica
        mostUsedTechnique = ''
        for i in range(1,lt.size(artworksSubSets)+1):
            subSet = lt.getElement(artworksSubSets,i)['artworks']
            technique = lt.getElement(techniques,i)
            sz = lt.size(subSet)
            sizeArtworks += sz
            if sz > maxValue:
                maxValue = sz
                mostUsedTechnique = technique



        # Imprimimos...
        print(f'{artistName} tiene {sizeArtworks} obras a su nombre en el museo.')
        print(f'Hay {sizeTechniques} técnicas diferentes en su trabajo.')
        print(f'Su técnica más utilizada fue: {mostUsedTechnique}, con un total de {maxValue} obras.')
        print()

        print(f'Las obras de la técnica {mostUsedTechnique} son...')
        print('Título\t\tFecha\t\tTécnica (medio)\t\tDimensiones')
        entry = mp.get(techniquesMap,mostUsedTechnique)
        mostUsedSubset = me.getValue(entry)
        for i in range(1,maxValue+1):
            artwork = lt.getElement(mostUsedSubset['artworks'],i)
            title = artwork['Title']
            date = artwork['Date']
            medium = artwork['Medium']
            dimensions = artwork['Dimensions']
            print(f'{title}\t\t{date}\t\t{medium}\t\t{dimensions}')

        print()
        spt = time.process_time()
        etms = (spt-st)*1000
        print('El tiempo de ejecucion es ' + str(etms) + 'ms')
        print()

    elif int(inputs[0]) == 5: # Requerimiento 4
        st = time.process_time()
        nationalities,artworksSubSets = classifyArtworksByNationality(catalog)
        print('El top 10 de las nacionalidades es:')
        print('Nacionalidad\t\tTotal de obras')
        for i in range(1,11):
            nationality = lt.getElement(nationalities,i)
            totalArtworks = lt.size(lt.getElement(artworksSubSets,i)['artworks'])
            print(f'{nationality}\t\t{totalArtworks}')

        print()

        print(f'Las primeras y últimas tres obras de la nacionalidad {lt.getElement(nationalities,1)} son...')
        print('Título\t\tArtista(s)\t\tFecha\t\tMedio\t\tDimensiones')
        selectedArtworks = lt.getElement(artworksSubSets,1)['artworks']
        size = lt.size(selectedArtworks)
        firstAndLast = [1, 2, 3, size - 2, size - 1, size]
        for i in firstAndLast:
            artwork = lt.getElement(selectedArtworks, i)
            title = artwork['Title']
            constituentID = artwork['ConstituentID'][1:-1].split(',')
            artists = []
            for id in constituentID:
                for artist in catalog['artists']['elements']:
                    if artist['ConstituentID'] == id:
                        artists.append(artist['DisplayName'])
                        break

            artists = ', '.join(artists)
            date = artwork['Date']
            medium = artwork['Medium']
            dimensions = artwork['Dimensions']
            print(f'{title}\t\t{artists}\t\t{date}\t\t{medium}\t\t{dimensions}')

        print()
        spt = time.process_time()
        etms = (spt-st)*1000
        print('El tiempo de ejecucion es ' + str(etms) + 'ms')
        print()

    elif int(inputs[0]) == 6: # Requerimiento 5
        department = input('Ingrese el departamento: ')
        st = time.process_time()
        selectedArtworks = getArtworksByDepartment(catalog,department)
        totalCost,totalWeight,selectedArtworks = estimateCosts(selectedArtworks)
        sizeArtworks = lt.size(selectedArtworks)
        fiveOldest = pickFiveOldestArtworks(selectedArtworks)
        fiveMostExpensive = pickFiveMostExpensive(selectedArtworks)

        print(f'Se transportarán {sizeArtworks} piezas desde el departamento {department}.')
        print('Recuerde que no todos los datos están completos. Estos son sólo estimados.')
        print(f'Costo estimado de la carga (USD): {totalCost}.')
        print(f'Peso estimado de la carga (kg): {totalWeight}.')
        print('Las 5 obras más antiguas a transportar son...')

        print('Título\t\tArtista(s)\t\tClasificación\t\tFecha\t\tMedio\t\tDimensiones\t\tCosto')

        for i in range(1,6):
            artwork = lt.getElement(fiveOldest, i)
            title = artwork['Title']
            constituentID = artwork['ConstituentID'][1:-1].split(',')
            artists = []
            for id in constituentID:
                for artist in catalog['artists']['elements']:
                    if artist['ConstituentID'] == id:
                        artists.append(artist['DisplayName'])
                        break

            artists = ', '.join(artists)
            classification = artwork['Classification']
            date = artwork['Date']
            medium = artwork['Medium']
            dimensions = artwork['Dimensions']
            cost = artwork['Cost']
            print(f'{title}\t\t{artists}\t\t{classification}\t\t{date}\t\t{medium}\t\t{dimensions}\t\t{cost}')

        print()

        print('Las 5 obras más costosas a transportar son...')

        print('Título\t\tArtista(s)\t\tClasificación\t\tFecha\t\tMedio\t\tDimensiones\t\tCosto')

        for i in range(1, 6):
            artwork = lt.getElement(fiveMostExpensive, i)
            title = artwork['Title']
            constituentID = artwork['ConstituentID'][1:-1].split(',')
            artists = []
            for id in constituentID:
                for artist in catalog['artists']['elements']:
                    if artist['ConstituentID'] == id:
                        artists.append(artist['DisplayName'])
                        break

            artists = ', '.join(artists)
            classification = artwork['Classification']
            date = artwork['Date']
            medium = artwork['Medium']
            dimensions = artwork['Dimensions']
            cost = artwork['Cost']
            print(f'{title}\t\t{artists}\t\t{classification}\t\t{date}\t\t{medium}\t\t{dimensions}\t\t{cost}')

        print()
        spt = time.process_time()
        etms = (spt-st)*1000
        print('El tiempo de ejecucion es ' + str(etms) + 'ms')
        print()
        
    elif int(inputs[0]) == 7: # Requerimiento 6
        year1 = input('Ingrese el año inicial de la exposición: ')
        year2 = input('Ingrese el año final de la exposición: ')
        areaMax = input('Ingrese el área disponible para la exposición (m^2): ')

        areaInUse, selectedArtworks = getArtworksByYearAndArea(catalog,year1,year2,areaMax)
        sizeArtworks = lt.size(selectedArtworks)

        print(f'Se hará una nueva exposición de piezas entre {year1} y {year2}.')
        print(f'Hay {sizeArtworks} obras posibles para un área disponible de {areaMax} m^2.')
        print(f'El área aproximadamente utilizada será de {areaInUse} m^2.')
        print()

        print('Las primeras y últimas 5 obras a exibir serán...')
        print('Título\t\tArtista(s)\t\tFecha\t\tClasificación\t\tMedio\t\tDimensiones')
        firstAndLast = [1,2,3,4,5,sizeArtworks-4,sizeArtworks-3,sizeArtworks-2,sizeArtworks-1,sizeArtworks]
        for i in firstAndLast:
            artwork = lt.getElement(selectedArtworks,i)
            title = artwork['Title']
            constituentID = artwork['ConstituentID'][1:-1].split(',')
            artists = []
            for id in constituentID:
                for artist in catalog['artists']['elements']:
                    if artist['ConstituentID'] == id:
                        artists.append(artist['DisplayName'])
                        break

            artists = ', '.join(artists)
            date = artwork['Date']
            classification = artwork['Classification']
            medium = artwork['Medium']
            dimensions = artwork['Dimensions']
            print(f'{title}\t\t{artists}\t\t{date}\t\t{classification}\t\t{medium}\t\t{dimensions}')
    elif int(inputs[0]) == 8:
        nationality = input('Ingrese la nacionalidad: ')
        selectedNationalities = getArtworksByNationality(catalog, nationality)
        
    else:
        sys.exit(0)
sys.exit(0)

