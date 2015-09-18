# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Canal para sports-main
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

__channel__ = "sports-main"
__title__ = "Deportes"
__language__ = "ES"

def isGeneric():
    return True


def mainlist(item):
    logger.info("[sports-main.py] mainlist")
    itemlist = []

    itemlist.append( Item(channel="sports-lshunter", action="mainlist", title="LSHunter.tv", url="http://www.drakulastream.eu" ))
    itemlist.append( Item(channel="sports-rojadirecta", action="mainlist", title="RojaDirecta.me", url="http://www.rojadirecta.me" ))
    #itemlist.append( Item(channel="sports-firstrow", action="mainlist", title="FirstRowSports.eu", url="http://www.ifeed2all.eu/type/football.html" ))
    
    itemlist.append( Item(channel="sports-lshunter", action="myteam", title=SPT.MIEQUIPO+" en LSHunter.tv", url="http://www.drakulastream.eu" ))
    itemlist.append( Item(channel="sports-rojadirecta", action="myteam", title=SPT.MIEQUIPO+" en RojaDirecta.me", url="http://www.rojadirecta.me" ))
    #itemlist.append( Item(channel="sports-firstrow", action="myteam", title=SPT.MIEQUIPO+" en FirstRowSports.eu", url="http://www.ifeed2all.eu/type/football.html" ))


    itemlist.append( Item(channel="configuracion", action="mainlist" , title="Configurar mi equipo : [COLOR=green][B]"+SPT.MIEQUIPO+'[/B][/COLOR]' ))

    return itemlist



# BUSCAR ENLACES A VIDEOS :
# =========================

def corregir_url(url):
    if url == 'http://tuttosportweb.com':
        return 'http://tuttosportweb.com/update/ch1.php'
    aux = scrapertools.find_single_match (url, "tuttosportweb.com/([\w]+.php)")
    if aux != '':
        return 'http://tuttosportweb.com/update/%s' % aux

    url = url.replace("kasimirotv.net/canal", "kasimirotv.net/player")

    return url

def play(item):
    logger.info("[sports-main.py] play")
    itemlist = []

    item.url = corregir_url(item.url)

    data = scrapertools.cachePage(item.url,headers=SPT.DEFAULT_HEADERS)

    headers = SPT.DEFAULT_HEADERS[:]
    headers.append(["Referer",item.url])

    url =  buscar_url_valida(data, headers)
    if url == '':
        # Buscar si hay algun iframe que pudiera contener el video (width>=500 y height>=300 !?)
        patron = '<iframe([^>]+)'
        matches = re.compile(patron,re.DOTALL | re.IGNORECASE).findall(data)
        for match in matches:
            #logger.info("iframe match "+match) # marginheight="0" marginwidth="0" style="width: 700px; height: 450px" width="650" height="80"
            w = re.findall ('[^n]width\s*[:=][^\d]*(\d+)', match, re.DOTALL | re.IGNORECASE)
            h = re.findall ('[^n]height\s*[:=][^\d]*(\d+)', match, re.DOTALL | re.IGNORECASE)
            if int(w[0]) >= 500 and int(h[0]) >= 300:
                url2 = scrapertools.find_single_match (match, 'src\s*=\s*["\']([^"\']+)')
                logger.info("buscando en iframe "+url2)

                headers = SPT.DEFAULT_HEADERS[:]
                headers.append(["Referer",item.url])
                try:
                    data = scrapertools.cachePage(url2,headers=headers)
                except:
                    continue
                if data == '':
                    continue

                headers = SPT.DEFAULT_HEADERS[:]
                headers.append(["Referer",url2])
                url =  buscar_url_valida(data, headers)
                if url != '':
                    break

    if url != '':
        itemlist.append( Item(channel=__channel__, title=item.title , url=url, server='directo'))
    else:
        logger.info("NO DETECTADO SERVIDOR")

    return itemlist


def buscar_url_valida(data, headers):
    logger.info("[sports-main.py] buscar_url_valida")
    if (SPT.DEBUG): logger.info("data="+data)

    # unescape de posible código javascript "oculto"
    patronjs = "unescape\s*\(\s*['\"]([^'\"]+)"
    matches = re.compile(patronjs,re.DOTALL).findall(data)
    for ofuscado in matches:
        data = data.replace(ofuscado, urllib.unquote(ofuscado))
    #if (SPT.DEBUG): logger.info("datanoofus="+data)

    # Ejecuta find_url_play en cada servidor hasta encontrar una url
    for serverid in SPT.SPORTS_SERVERS:
        try:
            servers_module = __import__("servers_sports."+serverid)
            server_module = getattr(servers_module,serverid)
            url = server_module.find_url_play(data, headers)
            if url != '':
                return url
        except ImportError:
            logger.info("No existe conector para "+serverid)
        except:
            logger.info("Error en el conector "+serverid)
            import traceback,sys
            from pprint import pprint
            exc_type, exc_value, exc_tb = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_tb)
            for line in lines:
                line_splits = line.split("\n")
                for line_split in line_splits:
                    logger.error(line_split)

    return '' # no encontrada
