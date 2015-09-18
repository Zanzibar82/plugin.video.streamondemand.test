# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para livego
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[livego.py] find_url_play")

    '''
<script type="text/javascript" src="http://www.livego.me/chaembed.php?id=jdfasjfasosihtord&width=680&height=450&autoplay=true">
    '''

    cid = scrapertools.find_single_match (data, "src=['\"]http://www.livego.me/chaembed.php\?id=([^&]+)")
    if cid == '':
        return ''

    url = 'rtmp://37.221.162.223:1935/go/_definst_/%s swfUrl=http://www.livego.tv/player/player-licensed.swf pageUrl=http://www.livego.tv/ live=true swfVfy=1 timeout=20' % cid
	
    return url
