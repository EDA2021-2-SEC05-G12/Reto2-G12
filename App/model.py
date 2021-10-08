"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """
    Inicializa el catálogo de obras y artistas. Crea una lista vacía para los artistas y otra vacía para las obras.
    """
    catalog = {'artists': lt.newList('ARRAY_LIST'),
               'artworks': lt.newList('ARRAY_LIST'),
               'mediums': mp.newMap(numelements=100, maptype='CHAINING', loadfactor=4.0),
               'nationalities': mp.newMap(numelements=500, maptype= 'CHAINING', loadfactor=4.0),
               'artistsIDs': mp.newMap(numelements=10000, maptype='PROBING', loadfactor=4.0)
               }

    return catalog


# Funciones para agregar informacion al catalogo

def addArtist(catalog,artist):
    """
    Se adiciona el artista al catálogo
    Args:
        catalog: Catálogo
        artist: Artista que se va a agregar
    """
    lt.addLast(catalog['artists'], artist)
    mp.put(catalog['artistsIDs'], artist['ConstituentID'], artist)

def addArtwork(catalog,artwork):
    """
    Se adiciona la obra al catálogo
    Args:
        catalog: Catálogo
        artwork: Obra que se va a agregar
    """
    lt.addLast(catalog['artworks'], artwork)
    addArtworkMedium(catalog, artwork)
    addArtworkNationality(catalog, artwork)

def addArtworkNationality(catalog, artwork):
    try:
        artistID = artwork['ConstituentID'][1:-1].split(',')[0]
        entry = mp.get(catalog['artistsIDs'], artistID)
        artist = me.getValue(entry)['artist']
        nationality_name = artist['Nationality']
        nationalities = catalog['nationalities']
        if (nationality == ''):
            medium_name = 'Unknown'
        existnationality = mp.contains(nationalities, nationality_name)
        if existnationality:
            entry = mp.get(nationalities, nationality_name)
            nationality = me.getValue(entry)
        else:
            nationality = newNationality(nationality_name)
            mp.put(nationalities, nationality_name, nationality)
        lt.addLast(nationality['artworks'], artworks)
    except Exception:
        return None

def newNationality(nationality_name):
    """
    Esta funcion crea la estructura de obras asociadas
    a una nacionalidad.
    """
    entry = {'nationality': "", "artworks": None}
    entry['nationality'] = nationality_name
    entry['artworks'] = lt.newList('ARRAY_LIST')
    return entry

def addArtworkMedium(catalog, artwork):

    try:
        mediums = catalog['mediums']
        if (artwork['Medium'] != ''):
            medium_name = artwork['Medium']
        else:
            medium_name = 'Unknown'
        existmedium = mp.contains(mediums, medium_name)
        if existmedium:
            entry = mp.get(mediums, medium_name)
            medium = me.getValue(entry)
        else:
            medium = newMedium(medium_name)
            mp.put(mediums, medium_name, medium)
        lt.addLast(medium['artworks'], artworks)
    except Exception:
        return None


def newMedium(medium_name):
    """
    Esta funcion crea la estructura de obras asociadas
    a un medio.
    """
    entry = {'medium': "", "artworks": None}
    entry['medium'] = medium_name
    entry['artworks'] = lt.newList('ARRAY_LIST')
    return entry
# Funciones para creacion de datos

# Funciones de consulta
def getArtistsByDates(catalog,year1,year2):
    """
    Selecciona una porción de la lista de artistas que cumplen con el rango de fechas
    Args:
        catalog: Catálogo de artistas y obras
        year1: Año inicial del rango
        year2: Año final del rango

    Returns: Lista de los artistas que cumplen

    """
    year1 = int(year1)
    year2 = int(year2)
    selectedArtists = lt.newList('ARRAY_LIST') #En esta lista se guardan los artistas que cumplen
    for artist in catalog['artists']['elements']:
        if year1 <= int(artist['BeginDate']) <= year2:
            lt.addLast(selectedArtists, artist)

    selectedArtists = sortArtists(selectedArtists)

    return selectedArtists

def getArtworksByDates(catalog,date1,date2):
    """
    Selecciona una porción de la lista de obras de arte que cumplen con el rango de fechas
    Args:
        catalog: El catálogo
        date1: Fecha inicial del rango
        date2: Fecha final del rango

    Returns: Lista con las obras que cumplen

    """
    # Pasamos las fechas a formato numérico
    date1 = int(''.join(date1.split('-')))
    date2 = int(''.join(date2.split('-')))
    selectedArtworks = lt.newList('ARRAY_LIST') #En esta lista se guardan las obras que cumplen
    for i in range(1,lt.size(catalog['artworks'])+1):
        artwork = lt.getElement(catalog['artworks'],i)
        if artwork['DateAcquired'] != '':
            date = int(''.join(artwork['DateAcquired'].split('-')))
            if date1 <= date <= date2:
                lt.addLast(selectedArtworks,artwork)

    selectedArtworks = sa.sort(selectedArtworks, compareArtworksByDateAcquired)

    return selectedArtworks

def countPurchasedArtworks(artworks):
    count = 0
    for i in range(1,lt.size(artworks)):
        artwork = lt.getElement(artworks,i)
        if artwork['CreditLine'] == 'Purchase':
            count += 1

    return count

def getArtworksByArtist(catalog,artistName):
    selectedArtist = None
    for i in range(1,lt.size(catalog['artists'])+1):
        artist = lt.getElement(catalog['artists'],i)
        if artist['DisplayName'] == artistName:
            selectedArtist = artist
            break

    constituentID = selectedArtist['ConstituentID']
    selectedArtworks = lt.newList('ARRAY_LIST')

    for i in range(1,lt.size(catalog['artworks'])+1):
        artwork = lt.getElement(catalog['artworks'],i)
        constituentIDs = artwork['ConstituentID'][1:-1].split(',')
        if constituentID in constituentIDs:
            lt.addLast(selectedArtworks,artwork)

    return selectedArtworks

def classifyArtworksByTechnique(artworks):
    techniques = []
    for artwork in artworks:
        technique = artwork['Medium']
        techniques.append(technique)

    techniques = list(set(techniques))
    artworksSubSets = lt.newList('ARRAY_LIST')
    for technique in techniques:
        subSet = lt.newList('ARRAY_LIST')
        for artwork in artworks:
            if artwork['Medium'] == technique:
                lt.addFirst(subSet,artwork)
        lt.addLast(artworksSubSets,subSet)

    return techniques,artworksSubSets

def classifyArtworksByNationality(catalog):
    nationalities = []
    for i in range(1,lt.size(catalog['artworks'])+1):
        artwork = lt.getElement(catalog['artworks'],i)
        constituentIDs = artwork['ConstituentID'][1:-1].split(',')
        for j in range(1,lt.size(catalog['artists'])+1):
            artist = lt.getElement(catalog['artists'],j)
            if artist['ConstituentID'] in constituentIDs:
                nationality = artist['Nationality']
                if nationality != "":
                    nationalities.append(nationality)

    nationalities = list(set(nationalities))
    artworksSubSet = lt.newList('ARRAY_LIST')
    for nationality in nationalities:
        subSet = lt.newList('ARRAY_LIST')
        for i in range(1,lt.size(catalog['artists'])+1):
            artist = lt.getElement(catalog['artists'],i)
            if artist['Nationality'] == nationality:
                for j in range(1,lt.size(catalog['artworks'])+1):
                    artwork = lt.getElement(catalog['artworks'], j)
                    constituentID = artwork['ConstituentID'][1:-1].split(',')[0]
                    if constituentID == artist['ConstituentID']:
                        lt.addLast(subSet,artwork)

        lt.addLast(artworksSubSet,subSet)

    # Organizamos los subsets y volvemos a buscar las nacionalidades para cada uno
    artworksSubSet = sa.sort(artworksSubSet,compareNationalities)
    nationalities = []
    for i in range(1,lt.size(artworksSubSet)+1):
        artwork = lt.getElement(lt.getElement(artworksSubSet,i),1)
        constituentID = artwork['ConstituentID'][1:-1].split(',')[0]
        for j in range(1,lt.size(catalog['artists'])+1):
            artist = lt.getElement(catalog['artists'],j)
            if artist['ConstituentID'] == constituentID:
                nationality = artist['Nationality']
                nationalities.append(nationality)
                break

    return nationalities,artworksSubSet


def getArtworksByDepartment(catalog,department):
    selectedArtworks = lt.newList('ARRAY_LIST')
    for i in range(1,lt.size(catalog['artworks'])+1):
        artwork = lt.getElement(catalog['artworks'],i)
        if artwork['Department'] == department:
            lt.addLast(selectedArtworks,artwork)

    return selectedArtworks

def estimateCosts(artworks):
    totalWeight = 0
    totalCost = 0
    for i in range(1,lt.size(artworks)+1):
        artwork = lt.getElement(artworks,i)
        weight = artwork['Weight (kg)']
        heightCm = artwork['Height (cm)']
        widthCm = artwork['Width (cm)']
        lengthCm = artwork['Length (cm)']
        costWeight = 0
        costVolume = 0
        costArea = 0
        if weight == "":
            weight = 0
        else:
            weight = float(weight)
            costWeight = 72*weight
        if heightCm != "" and widthCm != "":
            height = float(heightCm)/100
            width = float(widthCm)/100
            costArea = 72*height*width
            if lengthCm != "":
                length = float(lengthCm)/100
                costVolume = costArea*length

        cost = max([costWeight,costVolume,costArea])
        if cost == 0:
            cost = 48

        artwork['Cost'] = cost
        totalCost += cost
        totalWeight += weight


    return totalCost,totalWeight,artworks

def pickFiveOldestArtworks(artworks):
    sortedArtworks = sa.sort(artworks, compareArtworksByDate)
    fiveOldest = lt.subList(sortedArtworks,1,5)
    return fiveOldest

def pickFiveMostExpensive(artworks):
    sortedArtworks = sa.sort(artworks,compareArtworksByCost)
    fiveMostExpensive = lt.subList(sortedArtworks,1,5)
    return fiveMostExpensive

def getArtworksByYearAndArea(catalog,year1,year2,areaMax):
    areaMax = float(areaMax)
    department = 'Drawings & Prints'
    areaInUse = 0
    drawingsPrints = getArtworksByDepartment(catalog,department)
    selectedArtworks = lt.newList('ARRAY_LIST')
    for i in range(1,lt.size(drawingsPrints)+1):
        artwork = lt.getElement(drawingsPrints,i)
        year = artwork['Date']
        if year != '':
            if int(year1) <= int(year) <= int(year2):
                heightCm = artwork['Height (cm)']
                widthCm = artwork['Width (cm)']
                if heightCm != '' and widthCm != '':
                    height = float(heightCm)/100
                    width = float(widthCm)/100
                    area = height*width
                    if areaInUse + area <= areaMax:
                        lt.addLast(selectedArtworks,artwork)
                        areaInUse += area

    return areaInUse,selectedArtworks




# Funciones utilizadas para comparar elementos dentro de una lista

def compareArtists(artist1, artist2):
    """
    Retorna verdadero si el artista 1 nació antes que el artista 2.
    Args:
        artist1: Primer artista a comparar
        artist2: Segundo artista a comparar

    Returns: Booleano
    """

    result = int(artist1['BeginDate']) < int(artist2['BeginDate'])

    return result

def compareArtworksByDateAcquired(artwork1, artwork2):
    """
    Retorna verdadero si la fecha de adquisición de la primera obra es más antigua que la de la segunda obra
    Args:
        artwork1: Primera obra a comparar
        artwork2: Segunda obra a comparar

    Returns: Booleano

    """
    # La idea es convertir de un string 'AAAA-MM-DD' a un número AAAAMMDD, y que los compare
    date1 = int(''.join(artwork1['DateAcquired'].split('-')))
    date2 = int(''.join(artwork2['DateAcquired'].split('-')))

    result = date1 < date2

    return result

def compareArtworksByDate(artwork1,artwork2):
    date1 = artwork1['Date']
    date2 = artwork2['Date']

    return date1<date2

def compareArtworksByCost(artwork1,artwork2):

    cost1 = artwork1['Cost']
    cost2 = artwork2['Cost']
    return cost1 > cost2


def compareNationalities(set1,set2):
    return lt.size(set1) > lt.size(set2)

# Funciones de ordenamiento

def sortArtists(artists):
    """
    Ordena los artistas por fecha de nacimiento
    Args:
        artists: Lista de artistas

    Returns: Lista de artistas ordenada

    """
    artists = sa.sort(artists, compareArtists)
    return artists

def sortArtworks(artworks):
    """
    Ordena las obras por fecha de adquisición
    Args:
        artworks: Lista de obras de arte

    Returns: Lista de obras de arte ordenada
    """

    artworks = sa.sort(artworks, compareArtworksByDateAcquired)
    return artworks