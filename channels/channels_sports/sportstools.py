# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

from core import config

DEBUG = config.get_setting("debug")

# Nombre del equipo del que se buscan los enlaces
MIEQUIPO = config.get_setting("sportsmyteam")
if MIEQUIPO == '':
    MIEQUIPO = '(sin equipo)'

# Detección de enlaces en los siguientes servidores de deportes, ubicados en servers_sports
SPORTS_SERVERS = ['lshstream', '04stream', 'iguide', 'ucaster', 'ezcast']
SPORTS_SERVERS.extend( ['ustream', 'tutele', 'livego', 'myhdcast', 'goodcast'] )
SPORTS_SERVERS.extend( ['jjcast', 'liveall', 'leton', 'kingcast', 'megatvhd'] )

DEFAULT_HEADERS=[]
DEFAULT_HEADERS.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"])
DEFAULT_HEADERS.append(["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"])
DEFAULT_HEADERS.append(["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"])
DEFAULT_HEADERS.append(["Accept-Encoding","gzip, deflate"])


def formatear_server(nombre, estado=-1):
    if estado == -1: # determinar según si está o no en los servers
        estado = 1 if nombre.lower() in SPORTS_SERVERS else 2

    if estado == 1:
        return '[B]'+nombre+'[/B]'
    elif estado == 2:
        return '[COLOR=red]'+nombre+'[/COLOR]'
    else:
        return nombre

