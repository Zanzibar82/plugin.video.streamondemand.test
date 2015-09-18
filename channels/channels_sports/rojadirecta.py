# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Canal para sports-rojadirecta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools
from channels.channels_sports import sportstools as SPT

__channel__ = "sports-rojadirecta"
__title__ = "Roja Directa"
__language__ = "ES"

def isGeneric():
    return True

# ROJA DIRECTA
# ========================

def mainlist(item):
    logger.info("[sports-rojadirecta.py] mainlist")
    itemlist = []

    matches = get_events(item.url)
    for match in matches:
        #if (SPT.DEBUG): logger.info("match="+match)
        stime, sinfo, sname = extraer_titulo(match)
        titulo = stime + ' ' + sinfo + ' ' + sname

        itemlist.append( Item(channel=__channel__, action="event" , title=titulo , url=item.url, extra=sname ))

    return itemlist

def myteam(item):
    logger.info("[sports-rojadirecta.py] myteam")

    matches = get_events(item.url)
    for match in matches:
        #if (SPT.DEBUG): logger.info("match="+match)
        stime, sinfo, sname = extraer_titulo(match)
        if SPT.MIEQUIPO in sname:
            titulo = stime + ' ' + sinfo + ' ' + sname

            return get_links(match, titulo)

    return []

def event(item):
    logger.info("[sports-rojadirecta.py] event")

    matches = get_events(item.url)
    for match in matches:
        #if (SPT.DEBUG): logger.info("match="+match)
        stime, sinfo, sname = extraer_titulo(match)
        if sname == item.extra:
            titulo = stime + ' ' + sinfo + ' ' + sname

            return get_links(match, titulo)

    return []


# Devuelve un array con todos los eventos encontrados
def get_events(url):
    logger.info("[sports-rojadirecta.py] get_events")

    data = scrapertools.cachePage(url,headers=SPT.DEFAULT_HEADERS)
    if (SPT.DEBUG): logger.info("data="+data)
    data = data.decode('iso-8859-1').encode('utf8')

    patron = 'itemtype="http://schema.org/SportsEvent">(.*?)</table>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (SPT.DEBUG): logger.info("MATCHES="+str(len(matches)))

    return matches

# Devuelve una lista de links para un evento concreto
def get_links(match, plot=""):
    logger.info("[sports-rojadirecta.py] get_links")
    itemlist = []

    patron2 = '<tr>\s*<td>NO</td>\s*<td>(?!bwin|bet365)([^<]*)</td>\s*<td>([^<]*)</td>\s*<td>([^<]*).*?</td>\s*<td>(.*?)</td>\s*<td>(?:<b>)?<a[^>]*href="([^"]+)"'
    matches2 = re.compile(patron2,re.DOTALL).findall(match)
    for nombre,idioma,tipo,calidad,enlace in matches2:
        tipo = tipo.strip()
        calidad = calidad.replace('<!--9000-->','').replace(' (<span class="es">e</span>stable)','')
        titulo = nombre + ' - ' + idioma + ' - ' + calidad + ' kbps - ' + SPT.formatear_server(tipo)
        url = enlace.replace('#www.rojadirecta.me','').replace('goto/','http://')
        itemlist.append( Item(channel="sports-main", action="play" , title=titulo , url=url, plot=plot, extra=calidad))

    return sorted(itemlist, key=lambda k: int(k.extra), reverse=True) #ordenada por calidad
    #return itemlist


def extraer_titulo(match):
    stime, sinfo, sname = scrapertools.find_single_match(match,'<span class="t">([^<]+)</span></time>(.*?)<span itemprop="name">(.*?)</div>')

    sinfo = re.sub(r'<span class="es">([^<]*)</span>', r'\1', sinfo)
    sinfo = re.sub(r'(<span class="[^"]*">[^<]*</span>)', '', sinfo)
    sinfo = re.sub(r'<[^>]*>', '', sinfo)

    sname = re.sub(r'<span class="es">([^<]*)</span>', r'\1', sname)
    sname = re.sub(r'(<span class="[^"]*">[^<]*</span)>', '', sname)
    sname = re.sub(r'<[^>]*>', '', sname)

    return stime, sinfo.strip(), sname.strip()
