# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para streamingfilmit (ocultador de url)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_hops(url):
    redirect_re = re.compile('<meta[^>]*?url=(.*?)["\']', re.IGNORECASE)
    hops = []
    while url:
        if url in hops:
            url = None
        else:
            hops.insert(0, url)
            response = urllib2.urlopen(url)
            if response.geturl() != url:
                hops.insert(0, response.geturl())
            # check for redirect meta tag
            match = redirect_re.search(response.read())
            if match:
                url = urlparse.urljoin(url, match.groups()[0].strip())
            else:
                url = None
    return hops

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[streamingfilmit.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []
    
    patronvideos  = '(streamingfilmit.com/goto/[a-zA-Z0-9]+)'
    logger.info("[streamingfilmit.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streamingfilmit]"
        url = "http://www."+match
        #url = get_hops(url)
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'streamingfilmit' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
