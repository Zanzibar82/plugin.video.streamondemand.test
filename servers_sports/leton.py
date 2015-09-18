# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para leton
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[leton.py] find_url_play")

    pageurl = scrapertools.find_single_match (data, '["\'](http://leton.tv/player[^"\']+)"')
    if pageurl == '':
        return ''

    data2 = scrapertools.cachePage(pageurl, headers=headers)
    if (DEBUG): logger.info("data2="+data2)

    a,b,c,d,f,v = scrapertools.find_single_match(data2,"var a = ([^;]+);\s*var b = ([^;]+);\s*var c = ([^;]+);\s*var d = ([^;]+);\s*var f = ([^;]+);\s*var v_part = '([^']+)'")
    fileurl = 'rtmp://%d.%d.%d.%d%s' % (int(a)/int(f),int(b)/int(f),int(c)/int(f),int(d)/int(f),v)
    url = fileurl + ' swfUrl=http://files.leton.tv/jwplayer.flash.swf live=1 timeout=15 swfVfy=1 pageUrl=' + pageurl
    
    return url
