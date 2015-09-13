# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para streamingfilmit
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "streamingfilmit"
__category__ = "F"
__type__ = "generic"
__title__ = "Streamingfilmit.com (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

sito="http://www.streamingfilmit.com"

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.streamingfilmit mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Ultimi Film Inseriti[/COLOR]", action="peliculas", url="http://www.streamingfilmit.com/", thumbnail="http://dc584.4shared.com/img/XImgcB94/s7/13feaf0b538/saquinho_de_pipoca_01"))
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Film Per Categoria[/COLOR]", action="categorias", url="http://www.streamingfilmit.com/", thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png"))
    itemlist.append( Item(channel=__channel__, title="[COLOR yellow]Cerca...[/COLOR]", action="search", thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"))

    
    return itemlist

def categorias(item):
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    bloque = scrapertools.get_match(data,'<ul>(.*?)</ul>')
    
    # Extrae las entradas (carpetas)
    patron  = '<a href="(.*?)" >(.*?)</a>(.*?)\s*</li>'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedtot in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("Animazione",""))
        scrapedurl=scrapertools.decodeHtmlentities(scrapedurl.replace("http://www.streamingfilmit.com/category/animazione/",""))
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"]")
        itemlist.append( Item(channel=__channel__, action="pelicat", title="[COLOR azure]"+scrapedtitle+"[/COLOR][COLOR gray]" +scrapedtot+"[/COLOR]" , url=scrapedurl , thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png", folder=True) )

    return itemlist

def search(item,texto):
    logger.info("[streamingfilmit.py] "+item.url+" search "+texto)
    item.url = "http://www.streamingfilmit.com/?s="+texto
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item):
    logger.info("pelisalacarta.streamingfilmit peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<a title="(.*?)" href="(.*?)">\s*'
    patron += '<[^>]+>\s*'
    patron += '<[^>]+>\s*'
    patron += '<img[^=]+=[^=]+=[^=]+="(.*?)"[^>]+>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle,scrapedurl,scrapedthumbnail in matches:
        response = urllib2.urlopen(scrapedurl)
        html = response.read()
        start = html.find("<div id=\"detay-aciklama\">")
        end = html.find("</p>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        #scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title="[COLOR azure]"+scrapedtitle+"[/COLOR]" , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = '<a class="nextpostslink" rel="next" href="(.*?)">&raquo;</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="[COLOR orange]Successivo>>[/COLOR]" , url=scrapedurl , thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png", folder=True) )

    return itemlist

def pelicat(item):
    logger.info("pelisalacarta.streamingfilmit pelicat")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<div class="kapsa">\s*'
    patron += '<a href="(.*?)">\s*'
    patron += '<[^>]+>\s*'
    patron += '<[^>]+>\s*'
    patron += '<img[^=]+=[^=]+=[^=]+="(.*?)"[^>]+>\s*'
    patron += '<[^>]+>\s*'
    patron += '<[^>]+>\s*'
    patron += '[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>\s*'
    patron += '<[^>]+>\s*'
    patron += '<[^>]+>\s*'
    patron += '<h4><a[^>]+>(.*?)</a></h4>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        response = urllib2.urlopen(scrapedurl)
        html = response.read()
        start = html.find("<div id=\"detay-aciklama\">")
        end = html.find("</p>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        #scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title="[COLOR azure]"+scrapedtitle+"[/COLOR]" , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = '<a class="nextpostslink" rel="next" href="(.*?)">&raquo;</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="pelicat", title="[COLOR orange]Successivo>>[/COLOR]" , url=scrapedurl , thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png", folder=True) )

    return itemlist

