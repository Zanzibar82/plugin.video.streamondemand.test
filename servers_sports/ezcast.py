# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para ezcast
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[ezcast.py] find_url_play")

    '''
<script type='text/javascript'> width=500, height=400, channel='xxx', g='1';</script><script type='text/javascript' src='http://www.embedezcast.com/static/scripts/ezcast.js'></script>

<script type='text/javascript'> width=726, height=500, channel='danysportscoru', g='1';</script><script type='text/javascript' src='http://www.ezcast.tv/static/scripts/ezcast.js'></script>
    '''

    #fid = scrapertools.find_single_match (data, "channel=['\"]([^'\"]+)['\"].*?<script type=['\"]text/javascript['\"] src=['\"]http://www.embedezcast.com/static/scripts/ezcast.js['\"]")
    fid = scrapertools.find_single_match (data, "channel=['\"]([^'\"]+)['\"][^<]+</script><script type=['\"]text/javascript['\"] src=['\"]http://www.embedezcast.com/static/scripts/ezcast.js['\"]")
    if fid == '':
        fid = scrapertools.find_single_match (data, "channel=['\"]([^'\"]+)['\"][^<]+</script><script type=['\"]text/javascript['\"] src=['\"]http://www.ezcast.tv/static/scripts/ezcast.js['\"]")
        if fid == '':
            return ''

    pageurl = 'http://www.embedezcast.com/embedded/%s/1/500/400' % fid  # http://www.embedezcast.com/embedded/xxx/1/500/400
    data2 = scrapertools.cachePage(pageurl, headers=headers)
    if (DEBUG): logger.info("data2="+data2)

    '''
                <script type="text/javascript" src="/static/scripts/swfobject.js"></script>
                <div id="flashcontent">
                    <strong>You need to upgrade your Flash Player in order to watch movies from ezcast.tv</strong>
                </div>
                <script type="text/javascript">
                    var so = new SWFObject("/static/scripts/fplayer.swf", "fplayer", "500", "400", "9");
                    so.addParam('allowfullscreen','true');
                    so.addParam('allowscriptaccess','always');
                    so.addParam('wmode','transparent');
                    so.addParam('FlashVars', 'id=channelid&s=channelname&g=1&a=1&l=');
                    so.write("flashcontent");
                </script>
    '''

    data3 = scrapertools.cache_page('http://www.embedezcast.com:1935/loadbalancer',headers=headers)
    rtmpurl = 'rtmp://' + scrapertools.find_single_match (data3, "redirect=(.*)") + '/live'

    idvalue, svalue = scrapertools.find_single_match (data2, "'FlashVars', 'id=([^&]+)&s=([^&]+)")

    swfurl = 'http://www.embedezcast.com' + scrapertools.find_single_match (data2, 'new SWFObject\("([^"]+)"')

    url = '%s playpath=%s?id=%s swfVfy=1 timeout=15 conn=S:OK live=true swfUrl=%s pageUrl=%s' % (rtmpurl, svalue, idvalue, swfurl, pageurl)
    #url = '%s playpath=%s?id=%s timeout=15 conn=S:OK live=1 swfUrl=%s pageUrl=%s --live' % (rtmpurl, svalue, idvalue, swfurl, pageurl)

    return url
