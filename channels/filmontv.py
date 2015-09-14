# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Canal para filmontv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "filmontv"
__category__ = "F"
__type__ = "generic"
__title__ = "filmontv.tv (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("streamondemand.filmontv mainlist")
    itemlist = []

    itemlist.append( Item(channel=__channel__, title="[COLOR red]IN ONDA ADESSO[/COLOR]", action="tvoggi", url="http://www.comingsoon.it/filmtv/", thumbnail="http://a2.mzstatic.com/eu/r30/Purple/v4/3d/63/6b/3d636b8d-0001-dc5c-a0b0-42bdf738b1b4/icon_256.png"))
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Mattina[/COLOR]", action="tvoggi", url="http://www.comingsoon.it/filmtv/?range=mt", thumbnail="http://www.creattor.com/files/23/787/morning-pleasure-icons-screenshots-17.png"))
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Pomeriggio[/COLOR]", action="tvoggi", url="http://www.comingsoon.it/filmtv/?range=pm", thumbnail="http://icons.iconarchive.com/icons/custom-icon-design/weather/256/Sunny-icon.png"))
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Preserale[/COLOR]", action="tvoggi", url="http://www.comingsoon.it/filmtv/?range=pr", thumbnail="https://s.evbuc.com/https_proxy?url=http%3A%2F%2Ftriumphbar.com%2Fimages%2Fhappyhour_icon.png&sig=ADR2i7_K2FSfbQ6b3dy12Xjgkq9NCEdkKg"))
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Prima serata[/COLOR]", action="tvoggi", url="http://www.comingsoon.it/filmtv/?range=ps", thumbnail="http://icons.iconarchive.com/icons/icons-land/vista-people/256/Occupations-Pizza-Deliveryman-Male-Light-icon.png"))
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Seconda serata[/COLOR]", action="tvoggi", url="http://www.comingsoon.it/filmtv/?range=ss", thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"))
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Notte[/COLOR]", action="tvoggi", url="http://www.comingsoon.it/filmtv/?range=nt", thumbnail="http://icons.iconarchive.com/icons/oxygen-icons.org/oxygen/256/Status-weather-clear-night-icon.png"))

    return itemlist

def tvoggi(item):
    logger.info("streamondemand.filmontv tvoggi")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    
    # Extrae las entradas (carpetas)
    patron  = '<img src=\'(.*?)\'[^>]+>\s*</div>\s*<div[^>]+>[^>]+>\s*<div[^>]+>\s*<h3 >(.*?)</h3>\s*<div[^>]+>[^>]+>[^>]+>(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedthumbnail,scrapedtitle,scrapedtv in matches:
        scrapedplot = ""
        scrapedurl = ""
        #space = " "
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        titolo = scrapedtitle.replace(" ","+")
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"]")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle + "[COLOR yellow]   " + scrapedtv + "[/COLOR]" , url=scrapedurl , thumbnail=scrapedthumbnail, folder=True) )

    return itemlist


# Esta es la función que realmente realiza la búsqueda

def do_search(item):
    logger.info("streamondemand.channels.buscador do_search")

    tecleado = item.extra
    mostra = tecleado.replace("+"," ")

    itemlist = []

    import os
    import glob
    import imp

    master_exclude_data_file = os.path.join( config.get_runtime_path() , "resources", "filmontv.txt")
    logger.info("streamondemand.channels.buscador master_exclude_data_file="+master_exclude_data_file)

    exclude_data_file = os.path.join( config.get_data_path() , "filmontv.txt")
    logger.info("streamondemand.channels.buscador exclude_data_file="+exclude_data_file)

    channels_path = os.path.join( config.get_runtime_path() , "channels" , '*.py' )
    logger.info("streamondemand.channels.buscador channels_path="+channels_path)

    excluir=""

    if os.path.exists(master_exclude_data_file):
        logger.info("streamondemand.channels.buscador Encontrado fichero exclusiones")

        fileexclude = open(master_exclude_data_file,"r")
        excluir= fileexclude.read()
        fileexclude.close()
    else:
        logger.info("streamondemand.channels.buscador No encontrado fichero exclusiones")
        excluir = "seriesly\nbuscador\ntengourl\n__init__"

    if config.is_xbmc():
        show_dialog = True

    try:
        import xbmcgui
        progreso = xbmcgui.DialogProgressBG()
        progreso.create("Ricerca di "+ mostra.title())
    except:
        show_dialog = False

    channel_files = glob.glob(channels_path)
    number_of_channels = len(channel_files)

    for index, infile in enumerate(channel_files):
        percentage = index*100/number_of_channels

        basename = os.path.basename(infile)
        basename_without_extension = basename[:-3]
        
        if basename_without_extension not in excluir:

            if show_dialog:
                progreso.update(percentage, ' Sto cercando "' + mostra+ '"')

            logger.info("streamondemand.channels.buscador Tentativo di ricerca su " + basename_without_extension + " per "+ mostra)
            try:

                # http://docs.python.org/library/imp.html?highlight=imp#module-imp
                obj = imp.load_source(basename_without_extension, infile)
                logger.info("streamondemand.channels.buscador cargado " + basename_without_extension + " de "+ infile)
                channel_result_itemlist = obj.search( Item() , tecleado)
                for item in channel_result_itemlist:
                    item.title = item.title + " [COLOR green]Guarda in streaming[/COLOR]"
                    item.viewmode = "list"

                itemlist.extend( channel_result_itemlist )
            except:
                import traceback
                logger.error( traceback.format_exc() )

        else:
            logger.info("streamondemand.channels.buscador do_search_results, Escluso il server " + basename_without_extension)

    itemlist = sorted(itemlist, key=lambda Item: Item.title) 

    if show_dialog:
        progreso.close()

    return itemlist

