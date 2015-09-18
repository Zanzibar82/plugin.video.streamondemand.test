# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para iguide
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[iguide.py] find_url_play")

    fid = scrapertools.find_single_match (data, 'src="http://www.iguide.to/embed/([^&]+)') #http://www.iguide.to/embed/29586&width=730&height=430&autoplay=true
    if fid == '':
        return ''

    pageurl = 'http://www.iguide.to/embedplayer.php?width=730&height=430&channel=%s&autoplay=true' % fid
    data2 = scrapertools.cachePage(pageurl, headers=headers)
    if (DEBUG): logger.info("data2="+data2)

    '''
var token = "";
$.getJSON("http://www.iguide.to/serverfile.php?id=1422862766", function(json){
	token = json.token;
	setStream(token);
});

function setStream(token) {
	  jwplayer('dplayer').setup({
		'id': 'dplayer',
		'autostart': 'true',
		'width': '730',
		'height': '430',
		'controlbar':'bottom',
		'provider': 'rtmp',

		'streamer': 'rtmp://live2.iguide.to/redirect',
		'rtmp.tunneling':false,
 		'bufferLength':0.1,
		'file': '0zznd3dk4sqr3xg.flv',
		'modes': [
			{type: 'flash', src: 'http://www.iguide.to/player/secure_player_iguide_embed_token.swf'},
			{
			  type: 'html5',
			  config: {
			   'file': 'http://mobilestreaming.ilive.to:1935/edge/0zznd3dk4sqr3xg/playplist.m3u8',
			   'provider': 'video'
			  }
			}
		]
	  });
}
    '''

    #url = scrapertools.find_single_match (data2, "'file': '([^']+)'", 1)
    #return url

    tokenurl = scrapertools.find_single_match (data2, 'getJSON\("([^"]+)"')
    data3 = scrapertools.cache_page(tokenurl,headers=headers)
    if (DEBUG): logger.info("data3="+data3)
    tokenvalue = scrapertools.find_single_match (data3, '"token":"([^"]+)"')

    swfurl = 'http://www.iguide.to/player/secure_player_iguide_embed_token.swf'

    rtmpurl = scrapertools.find_single_match (data2, "'streamer': '([^']+)'")
    fileflv = scrapertools.find_single_match (data2, "'file': '([^'\.]+)")

    url = '%s playpath=%s swfUrl=%s live=1 token=%s timeout=15 swfVfy=1 pageUrl=%s' % (rtmpurl, fileflv, swfurl, tokenvalue, pageurl)
    
    return url
