# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para 04stream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def find_url_play(data, headers):
    logger.info("[04stream.py] find_url_play")

    fid = scrapertools.find_single_match (data, 'src="http://www.04stream.com/embed\.js\?stream=([^&]+)')
    if fid == '':
        return ''

    url = 'rtmp://46.246.29.130:1935/stream/%s.stream swfUrl=http://thecdn.04stream.com/p/ooolo1.swf live=true timeout=15 swfVfy=1' % fid
    
    return url
