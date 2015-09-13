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
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Film in TV oggi[/COLOR]", action="tvoggi", url="http://www.comingsoon.it/filmtv/", thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png"))
    
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

    itemlist = []

    import os
    import glob
    import imp

    master_exclude_data_file = os.path.join( config.get_runtime_path() , "resources", "global_search_exclusion.txt")
    logger.info("streamondemand.channels.buscador master_exclude_data_file="+master_exclude_data_file)

    exclude_data_file = os.path.join( config.get_data_path() , "global_search_exclusion.txt")
    logger.info("streamondemand.channels.buscador exclude_data_file="+exclude_data_file)

    channels_path = os.path.join( config.get_runtime_path() , "channels" , 'cineblog01.py' )
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
        progreso.create("Sto cercando "+ tecleado.title())
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
                progreso.update(percentage, ' Sto cercando "' + tecleado+ '"', basename_without_extension)

            logger.info("streamondemand.channels.buscador Provando a cercare in " + basename_without_extension + " per "+ tecleado)
            try:

                # http://docs.python.org/library/imp.html?highlight=imp#module-imp
                obj = imp.load_source(basename_without_extension, infile)
                logger.info("streamondemand.channels.buscador cargado " + basename_without_extension + " de "+ infile)
                channel_result_itemlist = obj.search( Item() , tecleado)
                for item in channel_result_itemlist:
                    item.title = item.title + " [COLOR grey][" + basename_without_extension + "][/COLOR]"
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

