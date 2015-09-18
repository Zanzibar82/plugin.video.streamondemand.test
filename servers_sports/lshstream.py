# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para lshstream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[lshstream.py] find_url_play")

    patron = 'fid=["\']([^"\']+)[^<]+</script><script type=["\']text/javascript["\'] src=["\']http://cdn.lshstream.com/embed.js["\']'

    fid = scrapertools.find_single_match (data, patron)
    if fid == '':
        return ''
    pageurl = 'http://cdn.lshstream.com/embed.php?u='+fid

    data2 = scrapertools.cachePage(pageurl, headers=headers)
    if (DEBUG): logger.info("data2="+data2)

    fileurl = scrapertools.find_single_match (data2, "file:'([^']+)'")
    url = fileurl + ' swfUrl=http://cdn.lshstream.com/jwplayer/jwplayer.flash.swf live=1 token=SECURET0KEN#yw%.?()@W! timeout=14 swfVfy=1 pageUrl=' + pageurl
    
    return url
