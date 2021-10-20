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
from DISClib.ADT import orderedmap as omp
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
               'mediums': mp.newMap(numelements=50, maptype='CHAINING', loadfactor=3.0),
               'nationalities': mp.newMap(numelements=300, maptype= 'PROBING', loadfactor=0.5),
               'artistsIDs': mp.newMap(numelements=40000, maptype='PROBING', loadfactor=0.9),
               'departments': mp.newMap(numelements=300, maptype='PROBING', loadfactor=0.5),
               'artistNames': mp.newMap(numelements=10000, maptype = 'PROBING', loadfactor = 4.0),
               'years': omp.newMap(),
               'dates': omp.newMap(),
               }

    return catalog


# Funciones para agregar informacion al catalogo

def addArtworkDepartment(catalog, artwork):

    try:
        departments = catalog['departments']
        if (artwork['Department'] != ''):
            department_name = artwork['Department']
        else:
            department_name = 'Unknown'
        existdepartment = mp.contains(departments, department_name)
        if existdepartment:
            entry = mp.get(departments, department_name)
            department = me.getValue(entry)
        else:
            department = newDepartment(department_name)
            mp.put(departments, department_name, department)
        lt.addLast(department['artworks'], artwork)
    except Exception:
        return None


def newDepartment(department_name):
    """
    Esta funcion crea la estructura de obras asociadas
    a un medio.
    """
    entry = {'department': "", "artworks": None}
    entry['department'] = department_name
    entry['artworks'] = lt.newList('ARRAY_LIST')
    return entry

def addArtist(catalog,artist):
    """
    Se adiciona el artista al catálogo
    Args:
        catalog: Catálogo
        artist: Artista que se va a agregar
    """
    lt.addLast(catalog['artists'], artist)
    mp.put(catalog['artistsIDs'], artist['ConstituentID'], artist)
    addArtistYear(catalog,artist)

def addArtistYear(catalog,artist):
    try:
        years = catalog['years']
        yearNumber = int(artist['BeginDate'])
        existYear = omp.contains(years, yearNumber)
        if existYear:
            entry = omp.get(years, yearNumber)
            year = me.getValue(entry)
        else:
            year = newYear(yearNumber)
            omp.put(years,yearNumber,year)
        lt.addLast(year['artists'],artist)

    except Exception:
        return None

def newYear(yearNumber):
    entry = {'year': yearNumber,
             'artists': lt.newList('ARRAY_LIST')}
    return entry

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
    addArtworkDepartment(catalog, artwork)
    addArtistName(catalog, artwork)
    addArtworkDate(catalog,artwork)

def addArtworkDate(catalog,artwork):
    try:
        dates = catalog['dates']
        dateInt = int(artwork['DateAcquired'].replace('-',''))
        dateExists = omp.contains(dates,dateInt)
        if dateExists:
            entry = omp.get(dates,dateInt)
            date = me.getValue(entry)
        else:
            date = newDate(dateInt)
            omp.put(dates,dateInt,date)
        lt.addLast(date['artworks'],artwork)
    except Exception:
        return None

def newDate(dateInt):
    entry = {'date': dateInt,
             'artworks': lt.newList('ARRAY_LIST')}
    return entry


def addArtworkNationality(catalog, artwork):
    try:
        artistID = artwork['ConstituentID'][1:-1].split(',')[0]
        entry = mp.get(catalog['artistsIDs'], artistID)
        artist = me.getValue(entry)
        nationality_name = artist['Nationality']
        nationalities = catalog['nationalities']
        if (nationality_name == ''):
            nationality_name = 'Unknown'
        existnationality = mp.contains(nationalities, nationality_name)
        if existnationality:
            entry = mp.get(nationalities, nationality_name)
            nationality = me.getValue(entry)
        else:
            nationality = newNationality(nationality_name)
            mp.put(nationalities, nationality_name, nationality)
        lt.addLast(nationality['artworks'], artwork)
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
        lt.addLast(medium['artworks'], artwork)
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

def addArtistName(catalog,artwork):
    try:
        artistNames = catalog['artistNames']
        artistID = artwork['ConstituentID'][1:-1].split(',')[0]
        entry = mp.get(catalog['artistsIDs'], artistID)
        artist = me.getValue(entry)
        artistName = artist['DisplayName']
        existArtist = mp.contains(artistNames,artistName)
        if existArtist:
            entry = mp.get(artistNames,artistName)
            artist = me.getValue(entry)
        else:
            artist = newArtist(artistName)
            mp.put(artistNames,artistName,artist)
        mediums = artist['mediums']
        mediumName = artwork['Medium']
        if mediumName == '':
            mediumName = 'Unknown'
        existMedium = mp.contains(mediums,mediumName)
        if existMedium:
            entry = mp.get(mediums,mediumName)
            medium = me.getValue(entry)
        else:
            medium = newMedium(mediumName)
            mp.put(mediums,mediumName,medium)
        lt.addLast(medium['artworks'],artwork)
    except:
        return None

def newArtist(artistName):
    entry = {'artistName': '', 'mediums': None}
    entry['artistName'] = artistName
    entry['mediums'] = mp.newMap(numelements=50, maptype='CHAINING', loadfactor=3.0)
    return entry

# Funciones para creacion de datos

# Funciones de consulta

def getArtistsByDates(catalog, year1, year2):
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
    artistSets = omp.values(catalog['years'],year1,year2)
    selectedArtists = lt.newList('ARRAY_LIST')
    for i in range(1,lt.size(artistSets)+1):
        set = lt.getElement(artistSets,i)['artists']
        for j in range(1,lt.size(set)+1):
            artist = lt.getElement(set,j)
            lt.addLast(selectedArtists,artist)

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
    date1 = int(date1.replace('-',''))
    date2 = int(date2.replace('-', ''))
    artworkSets = omp.values(catalog['dates'],date1,date2)
    selectedArtworks = lt.newList('ARRAY_LIST')
    for i in range(1,lt.size(artworkSets)+1):
        set = lt.getElement(artworkSets,i)['artworks']
        for j in range(1,lt.size(set)+1):
            artwork = lt.getElement(set,j)
            lt.addLast(selectedArtworks,artwork)

    return selectedArtworks


def countPurchasedArtworks(artworks):
    count = 0
    for i in range(1,lt.size(artworks)+1):
        artwork = lt.getElement(artworks,i)
        if artwork['CreditLine'] == 'Purchase':
            count += 1

    return count



def classifyArtworksByTechnique(catalog,artistName):
    selectedArtist = mp.get(catalog['artistNames'], artistName)
    techniquesMap = me.getValue(selectedArtist)['mediums']


    return techniquesMap

def classifyArtworksByNationality(catalog):
    nationalitiesMap = catalog['nationalities']
    artworksSubSets = mp.valueSet(nationalitiesMap)

    sortedArtworks = sa.sort(artworksSubSets,compareNationalities)
    sortedNationalities = lt.newList('ARRAY_LIST')
    for i in range(1,lt.size(sortedArtworks)+1):
        subset = lt.getElement(sortedArtworks,i)['artworks']
        constituentID = lt.getElement(subset,0)['ConstituentID'][1:-1].split(',')[0]
        artist = me.getValue(mp.get(catalog['artistsIDs'],constituentID))
        nationality = artist['Nationality']
        lt.addLast(sortedNationalities,nationality)

    return sortedNationalities, sortedArtworks



def getArtworksByDepartment(catalog,department):
    entry = mp.get(catalog['departments'], department)
    selectedArtworks = me.getValue(entry)['artworks']
    return selectedArtworks

def getArtworksByNationality(catalog,nationality):
    selectedNationalities = None
    entry = mp.get(catalog['nationalities'], nationality)
    selectedNationalities = me.getValue(entry)['artworks']
    return selectedNationalities

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
    return lt.size(set1['artworks']) > lt.size(set2['artworks'])


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