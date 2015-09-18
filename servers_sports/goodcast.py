# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para goodcast
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[goodcast.py] find_url_play")

    pageurl = scrapertools.find_single_match (data, "src=['\"](http://goodcast.co/stream[^'\"]+)")
    if pageurl == '':
        return ''

    data2 = scrapertools.cachePage(pageurl, headers=headers)
    if (DEBUG): logger.info("data2="+data2)

    '''
<object type="application/x-shockwave-flash" 
	data="http://cdn.goodcast.co/players.swf" 
	width="640" 
	height="480" 
	id="player">
		<param name="allowfullscreen" value="true">
		<param name="allowscriptaccess" value="always">
		<param name="wmode" value="opaque">
		<param name="flashvars" value="file=204232&amp;streamer=rtmp://130.180.201.114:80/liverepeater&amp;rtmp.fallback=false&amp;autostart=true">
		<embed id="player"
			src="http://cdn.goodcast.co/players.swf"
			width="640"
			height="480"
			allowscriptaccess="always"
			allowfullscreen="true"
			flashvars="file=204232&amp;streamer=rtmp://130.180.201.114:80/liverepeater&amp;rtmp.fallback=false&amp;autostart=true" />
</object>
    '''

    swfurl = 'http://cdn.goodcast.co/players.swf'
    tokenvalue = 'Fo5_n0w?U.rA6l3-70w47ch'

    filevalue, rtmpurl = scrapertools.find_single_match (data2, 'file=([^&]+)&amp;streamer=([^&]+)')

    url = '%s playpath=%s swfUrl=%s swfVfy=1 live=1 timeout=15 token=%s pageUrl=%s' % (rtmpurl, filevalue, swfurl, tokenvalue, pageurl)
    #url = '%s playpath=%s swfUrl=%s swfVfy=1 live=1 timeout=15 pageUrl=%s' % (rtmpurl, filevalue, swfurl, pageurl)

    return url
