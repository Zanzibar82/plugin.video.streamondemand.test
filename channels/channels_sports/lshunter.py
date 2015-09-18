# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Canal para sports-lshunter
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools
from pelisalacarta.channels_sports import sportstools as SPT

__channel__ = "sports-lshunter"
__title__ = "LSHunter"
__language__ = "IT"

def isGeneric():
    return True

# LSHUNTER / DRAKULASTREAM
# ========================

def mainlist(item):
    logger.info("[sports-lshunter.py] mainlist")
    itemlist = []

    matches = get_events(item.url)
    for match in matches:
        #if (SPT.DEBUG): logger.info("match="+match)
        scrapedtitle = scrapertools.find_single_match(match,'<span class="lshevent">([^<]+)</span>')
        scrapedtime = scrapertools.find_single_match(match,'<span class="lshstart_time">([^<]+)</span>')
        titulo = scrapedtime + ' ' + scrapertools.htmlclean(scrapedtitle.strip())
        scrapedurl = scrapertools.find_single_match(match,'<a class="open_event_tab" target="_blank" href="([^"]+)')
        scrapedurl = urlparse.urljoin(item.url, scrapedurl)

        itemlist.append( Item(channel=__channel__, action="event" , title=titulo , url=scrapedurl ))

    return itemlist

def myteam(item):
    logger.info("[sports-lshunter.py] myteam")

    matches = get_events(item.url)
    for match in matches:
        scrapedtitle = scrapertools.find_single_match(match,'<span class="lshevent">([^<]+)</span>')
        if SPT.MIEQUIPO in scrapedtitle:
            scrapedtime = scrapertools.find_single_match(match,'<span class="lshstart_time">([^<]+)</span>')
            plot = scrapedtime + ' ' + scrapertools.htmlclean(scrapedtitle.strip())

            return get_links(match, plot)

    return []

def event(item):
    logger.info("[sports-lshunter.py] event")

    data = scrapertools.cachePage(item.url,headers=SPT.DEFAULT_HEADERS)
    if (SPT.DEBUG): logger.info("data="+data)

    return get_links(data, item.title)


# Devuelve un array con todos los eventos encontrados
def get_events(url):
    logger.info("[sports-lshunter.py] get_events")

    data = scrapertools.cachePage(url,headers=SPT.DEFAULT_HEADERS)
    if (SPT.DEBUG): logger.info("data="+data)

    patron = '<!-- main container of a slide -->(.*?)<!-- close main container of a slide -->'    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (SPT.DEBUG): logger.info("MATCHES="+str(len(matches)))

    return matches

# Devuelve una lista de links para un evento concreto
def get_links(match, plot=""):
    logger.info("[sports-lshunter.py] get_links")
    itemlist = []

    matches2 = re.compile('<tr class="sectiontable([^"]+)">(.*?)</tr>',re.DOTALL).findall(match)
    for section,inner in matches2:
        if (SPT.DEBUG): logger.info("innerlshlinks="+inner)
        if section == 'header':
            section_name = scrapertools.find_single_match(inner,'<td>([^<]+)</td>')
        else:
            server_name = scrapertools.find_single_match(inner,'<td width="80"><a>([^:]+)')
            server_name_fmt = SPT.formatear_server(server_name, 1) if section_name != 'Other Links:' and server_name != 'Flash' else SPT.formatear_server(server_name)

            matches3 = re.compile('href=["\']javascript:openWindow\(["\']([^"\']+)',re.DOTALL | re.IGNORECASE).findall(inner)
            for n, scrapedurl in enumerate(matches3):
                desglose = scrapertools.find_single_match(scrapedurl,'event_id=([^&]+)&tv_id=([^&]+)&tid=([^&]+)&channel=([^&]+)&')
                if len(desglose) == 4:
                    event_id,tv_id,tid,chan = desglose
                else:
                    event_id,tid,chan = scrapertools.find_single_match(scrapedurl,'event_id=([^&]+)&tid=([^&]+)&channel=([^&]+)&')
                    tv_id = '0'
                url = 'http://live.drakulastream.eu/static/popups/%s%s%s%s.html' % (event_id,tv_id,tid,chan)
                titulo = section_name + ' [' + server_name_fmt + '~' + str(n+1) + ']'
                if (SPT.DEBUG): logger.info("LINK: "+section_name+" : "+server_name+" : "+scrapedurl+" :: "+url)
                itemlist.append( Item(channel="sports-main", action="play" , title=titulo , url=url, plot=plot))

            matches3 = re.compile('href=["\'](http://live.drakulastream.eu/players/[^"\']+)',re.DOTALL).findall(inner)
            for n, url in enumerate(matches3):
                titulo = section_name + ' ' + server_name_fmt + '-' + str(n+1)
                if (SPT.DEBUG): logger.info("LINK: "+section_name+" : "+server_name+" : "+url)
                itemlist.append( Item(channel="sports-main", action="play" , title=titulo , url=url, plot=plot))

    return itemlist


