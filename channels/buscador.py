# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand.- XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
#------------------------------------------------------------
import urlparse,urllib2,urllib,re,os,sys

from core import config
from core import logger
from core.item import Item
from core import scrapertools

__channel__ = "buscador"

logger.info("streamondemand.channels.buscador init")

DEBUG = True

def isGeneric():
    return True

def mainlist(item,preferred_thumbnail="squares"):
    logger.info("streamondemand.channels.buscador mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="search"  , title="[COLOR yellow]Effettuare una nuova ricerca...[/COLOR]" ))

    saved_searches_list = get_saved_searches(item.channel)

    for saved_search_text in saved_searches_list:
        itemlist.append( Item(channel=__channel__ , action="do_search"  , title=' "'+saved_search_text+'"', extra=saved_search_text ))

    if len(saved_searches_list)>0:
        itemlist.append( Item(channel=__channel__ , action="clear_saved_searches"  , title="[COLOR red]Elimina cronologia ricerche[/COLOR]" ))

    return itemlist

# Al llamar a esta función, el sistema pedirá primero el texto a buscar
# y lo pasará en el parámetro "tecleado"
def search(item,tecleado):
    logger.info("streamondemand.channels.buscador search")

    if tecleado!="":
        save_search(item.channel,tecleado)

    item.extra = tecleado
    return do_search(item)

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

    channels_path = os.path.join( config.get_runtime_path() , "channels" , '*.py' )
    logger.info("streamondemand.channels.buscador channels_path="+channels_path)

    excluir=""

    # El fichero que se distribuyó en la 4.0.2 no era completo
    '''
    if os.path.exists(exclude_data_file):
        fileexclude = open(exclude_data_file,"r")
        excluir= fileexclude.read()
        fileexclude.close()
    else:
        excluir = "seriesly\n"
        fileexclude = open(exclude_data_file,"w")
        fileexclude.write(excluir)
        fileexclude.close()
    '''
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

def save_search(channel,text):

    saved_searches_limit = ( 10, 20, 30, 40, )[ int( config.get_setting( "saved_searches_limit" ) ) ]

    if os.path.exists(os.path.join( config.get_data_path() , "saved_searches.txt" )):
        f = open( os.path.join( config.get_data_path() , "saved_searches.txt" ) , "r" )
        saved_searches_list = f.readlines()
        f.close()
    else:
        saved_searches_list = []

    saved_searches_list.append(text)

    if len(saved_searches_list)>=saved_searches_limit:
        # Corta la lista por el principio, eliminando los más recientes
        saved_searches_list = saved_searches_list[-saved_searches_limit:]

    f = open( os.path.join( config.get_data_path() , "saved_searches.txt" ) , "w" )
    for saved_search in saved_searches_list:
        f.write(saved_search+"\n")
    f.close()

def clear_saved_searches(item):

    f = open( os.path.join( config.get_data_path() , "saved_searches.txt" ) , "w" )
    f.write("")
    f.close()

def get_saved_searches(channel):

    if os.path.exists(os.path.join( config.get_data_path() , "saved_searches.txt" )):
        f = open( os.path.join( config.get_data_path() , "saved_searches.txt" ) , "r" )
        saved_searches_list = f.readlines()
        f.close()
    else:
        saved_searches_list = []

    # Invierte la lista, para que el último buscado salga el primero
    saved_searches_list.reverse()

    trimmed = []
    for saved_search_text in saved_searches_list:
        trimmed.append(saved_search_text.strip())
    
    return trimmed
