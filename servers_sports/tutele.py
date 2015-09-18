# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para tutele
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[tutele.py] find_url_play")

    '''
<script type='text/javascript'> width=700, height=420, channel='footmax1',   token=document.domain, e='1';</script><script type='text/javascript' src='http://tutelehd.com/embedPlayer.js'></script>
    '''

    fid = scrapertools.find_single_match (data, "channel=['\"]([^'\"]+)[^<]+</script><script type=['\"]text/javascript['\"] src=['\"]http://tutelehd.com/embedPlayer.js['\"]")
    #fid = scrapertools.find_single_match (data, "channel=['\"]([^'\"]+).*?<script type=['\"]text/javascript['\"] src=['\"]http://tutelehd.com/embedPlayer.js['\"]")
    if fid == '':
        return ''

    pageurl = 'http://tutelehd.com/embed/embed.php?channel=%s&w=700&h=420' % fid  # http://tutelehd.com/embed/embed.php?channel=footmax1&w=700&h=420
    data2 = scrapertools.cachePage(pageurl, headers=headers)
    if (DEBUG): logger.info("data2="+data2)

    '''
<script type="text/javascript">
                    var so = new SWFObject('/player.swf', 'jwplayer1', '100%', '100%', '8');
                    so.addParam('allowscriptaccess', 'always');
                    so.addParam('allowfullscreen', 'true');
                    so.addParam('wmode','opaque');
                    so.addVariable('logo', '');
                    so.addVariable('dock','false')
                    so.addVariable('autostart', 'true');
			        so.addVariable('token', '0fea41113b03061a');
                    so.addVariable('abouttext', 'Player http://tutelehd.com');
                    so.addVariable('aboutlink', 'http://tutelehd.com');
                    so.addVariable('file', 'footmax1');
                    so.addVariable('image', '');
                    so.addVariable('logo.link','http://tutelehd.com/');
                    so.addVariable('logo.position','top-right');
                    so.addVariable('stretching','exactfit');
                    so.addVariable('backcolor','000000');
                    so.addVariable('frontcolor','ffffff');
                    so.addVariable('screencolor','000000');
                    so.addVariable('streamer', 'rtmpe://live.tutelehd.com/redirect?token=lkTEmeABiFNVNxbjh9SgsAExpired=1422985939');
                    so.addVariable('provider', 'rtmp');
                    so.write('jwplayer1');
                          </script>
    '''

    swfurl = 'http://tutelehd.com' + scrapertools.find_single_match (data2, 'new SWFObject\(["\']([^"\']+)')
    filevalue = scrapertools.find_single_match (data2, '["\']file["\'][:,]\s*["\']([^"\']+)')
    rtmpurl = scrapertools.find_single_match (data2, '["\']streamer["\'][:,]\s*["\']([^"\']+)')
    tokenvalue = scrapertools.find_single_match (data2, '["\']token["\'][:,]\s*["\']([^"\']+)')

    #appvalue = scrapertools.find_single_match (rtmpurl, 'rtmpe://live.tutelehd.com/([^"\']+)')
    #url = '%s app=%s playpath=%s swfUrl=%s swfVfy=1 live=true token=%s flashver=WIN\\202012,0,0,77 pageUrl=%s' % (rtmpurl, appvalue, filevalue, swfurl, tokenvalue, pageurl)

    url = '%s playpath=%s swfUrl=%s swfVfy=1 live=true token=%s pageUrl=%s' % (rtmpurl, filevalue, swfurl, tokenvalue, pageurl)

    return url
