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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de artistas y obras
    Args:
        catalog: el catálogo


    """
    loadArtists(catalog)
    loadArtworks(catalog)

def loadArtists(catalog):
    """
    Carga los artistas del archivo

    """
    artistsfile = cf.data_dir + 'Artists-utf8-large.csv'
    input_file = csv.DictReader(open(artistsfile,encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog,artist)

def loadArtworks(catalog):
    """
    Carga las obras de arte del archivo
    """

    artworksfile = cf.data_dir + 'Artworks-utf8-large.csv'
    input_file = csv.DictReader(open(artworksfile,encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog,artwork)


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def getArtistsByDates(catalog,year1,year2):
    """
    Selecciona una porción de la lista de artistas que cumplen con el rango de fechas
    Args:
        catalog: Catálogo de artistas y obras
        year1: Año inicial del rango
        year2: Año final del rango

    Returns: Lista de los artistas que cumplen
    """

    return model.getArtistsByDates(catalog, year1, year2)

def getArtworksByDates(catalog,date1,date2):
    """
    Selecciona una porción de la lista de obras de arte que cumplen con el rango de fechas
    Args:
        catalog: Catálogo de artistas y obras
        date1: Fecha inicial del rango
        date2: Fecha final del rango

    Returns: Lista de las obras que cumplen

    """

    return model.getArtworksByDates(catalog, date1, date2)

def countPurchasedArtworks(artworks):
    """
    Cuenta las obras adquiridas mediante compra
    Args:
        artworks: Lista de obras de arte

    Returns: Total de obras

    """
    return model.countPurchasedArtworks(artworks)

def getArtworksByArtist(catalog,artistName):
    return model.getArtworksByArtist(catalog,artistName)

def classifyArtworksByTechnique(artworks):
    return model.classifyArtworksByTechnique(artworks)

def classifyArtworksByNationality(catalog):
    return model.classifyArtworksByNationality(catalog)

def getArtworksByDepartment(catalog,department):
    return model.getArtworksByDepartment(catalog,department)

def estimateCosts(artworks):
    return model.estimateCosts(artworks)

def pickFiveOldestArtworks(artworks):
    return model.pickFiveOldestArtworks(artworks)

def pickFiveMostExpensive(artworks):
    return model.pickFiveMostExpensive(artworks)

def getArtworksByYearAndArea(catalog,year1,year2,areaMax):
    return model.getArtworksByYearAndArea(catalog,year1,year2,areaMax)


