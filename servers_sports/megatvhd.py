# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para megatvhd
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[megatvhd.py] find_url_play")

    pageurl = scrapertools.find_single_match (data, "src=['\"](http://megatvhd.tv/roja.js)")
    if pageurl == '':
        return ''

    cid = scrapertools.find_single_match (data, 'id=["\']([^"\']+)')
    if cid == '':
        return ''
    pageurl = pageurl.replace('.js','.php?id=') + cid

    data2 = scrapertools.cachePage(pageurl, headers=headers)
    if (DEBUG): logger.info("data2="+data2)

    swfurl = 'http://megatvhd.tv/jsplayer/jwplayer.flash.swf'

    rtmpurl = scrapertools.find_single_match (data2, 'file:\s*["\']([^"\']+)')

    url = '%s swfUrl=%s swfVfy=1 live=1 timeout=15 pageUrl=%s' % (rtmpurl, swfurl, pageurl)

    return url
