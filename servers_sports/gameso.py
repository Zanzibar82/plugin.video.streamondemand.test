# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para gameso
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[gameso.py] find_url_play")

    fid = scrapertools.find_single_match (data, 'src="http://www.gameso.tv/embed\.php\?id=([^&]+)')
    if fid == '':
        return ''

    pageurl = 'http://www.gameso.tv/embedplayer.php?width=650&height=400&id=%s&autoplay=true' % fid
    data2 = scrapertools.cachePage(pageurl, headers=headers)
    if (DEBUG): logger.info("data2="+data2)

    # PDT ...
    '''
var token = "";
$.getJSON("http://www.gameso.tv/file.php?id=1422830635", function(json){
	token = json.token;
	setStream(token);
});
function setStream(token) {
		  jwplayer('dplayer').setup({
			'id': 'dplayer',
			'autostart': 'true',
			token: token,
			'rtmp.tunneling':false,
			'bufferLength':0.1,
			'width': '650',
			'height': '400',
			'controlbar':'bottom',
			'provider': 'rtmp',
			'streamer': 'rtmp://go.gameso.tv/fasts',
			'file': 'max2a6.flv',
			'modes': [
				{type: 'flash', src: 'http://www.gameso.tv/player/player_embed.swf'},
				{
				  type: 'html5',
				  config: {
				   'file': 'http',
				   'provider': 'video'
				  }
				}
			]
		  });
}
    '''

    streamer = ''
    fileflv = ''
    pageurl = ''
    token = '' # {"token":"#ed%h0#w18723jdsahjkDHF"}

    url = '%s/%s swfUrl=http://www.gameso.tv/player/player_embed.swf live=true token=%s timeout=15 swfVfy=1 pageUrl=%s' % (streamer, fileflv, token, pageurl)
    
    return url
