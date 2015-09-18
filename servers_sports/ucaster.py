# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para ucaster
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[ucaster.py] find_url_play")

    '''
<script type='text/javascript'> width=726, height=500, channel='danysportscucu', g='1';</script><script type='text/javascript' src='http://www.ucaster.eu/static/scripts/ucaster.js'></script>

<script type="text/javascript">
                                            <!--//--><![CDATA[// ><!--
                                             width=610, height=470, channel='tashsport02', g='1';
                                            //--><!]]>
                                            </script><script type="text/javascript" src="http://www.ucaster.eu/static/scripts/ucaster.js"></script>
    '''
    fid = scrapertools.find_single_match (data, "channel='([^']+)'[^<]+</script><script type='text/javascript' src='http://www.ucaster.eu/static/scripts/ucaster.js'")
    if fid == '':
        fid = scrapertools.find_single_match (data, "channel='([^']+)'[^<]+<[^<]+</script><script type=['\"]text/javascript['\"] src=['\"]http://www.ucaster.eu/static/scripts/ucaster.js['\"]")
        if fid == '':
            return ''

    pageurl = 'http://www.embeducaster.com/embedded/%s/1/726/500' % fid  #http://www.embeducaster.com/embedded/danysportscucu/1/726/500
    data2 = scrapertools.cachePage(pageurl, headers=headers)
    if (DEBUG): logger.info("data2="+data2)

    '''
        <div class="player_div"  align="center">
            <span>
                <script type="text/javascript" src="/static/scripts/swfobject.js"></script>
                <div id="flashcontent">
                    <strong>You need to upgrade your Flash Player in order to watch movies from ucaster.eu</strong>
                </div>
                <script type="text/javascript">
                    var so = new SWFObject("/static/scripts/fplayer.swf", "fplayer", "726", "500", "9");
                    so.addParam('allowfullscreen','true');
                    so.addParam('allowscriptaccess','always');
                    so.addParam('wmode','transparent');
                    so.addParam('FlashVars', 'id=78955&s=danysportscucu&g=1&a=1&l=Dany Rojadirecta.me');
                    so.write("flashcontent");
                </script>
            </span>
        </div>
    '''

    data3 = scrapertools.cache_page('http://www.embeducaster.com:1935/loadbalancer',headers=headers)
    rtmpurl = 'rtmp://' + scrapertools.find_single_match (data3, "redirect=(.*)") + '/live'

    idvalue, svalue = scrapertools.find_single_match (data2, "'FlashVars', 'id=([^&]+)&s=([^&]+)")

    swfurl = 'http://www.embeducaster.com' + scrapertools.find_single_match (data2, 'new SWFObject\("([^"]+)"')

    url = '%s playpath=%s?id=%s swfUrl=%s swfVfy=1 conn=S:OK live=1 pageUrl=%s' % (rtmpurl, svalue, idvalue, swfurl, pageurl)
    #url = '%s playpath=%s?id=%s swfUrl=%s conn=S:OK live=1 timeout=20 pageUrl=%s --live' % (rtmpurl, svalue, idvalue, swfurl, pageurl)
    
    return url
