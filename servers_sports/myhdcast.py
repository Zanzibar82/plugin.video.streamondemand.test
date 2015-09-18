# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para myhdcast
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[myhdcast.py] find_url_play")

    #<iframe src='http://myhdcast.com/embedplayer.php?width=653&height=410&id=astr5&autoplay=true'

    pageurl = scrapertools.find_single_match (data, "src=['\"](http://myhdcast.com/embedplayer.php[^'\"]+)")
    if pageurl == '':
        cid = scrapertools.find_single_match (data, "src=['\"]http://www.myhdcast.com/embed.php([^'\"]+)")
        if cid == '':
            return ''
        pageurl = 'http://myhdcast.com/embedplayer.php%s' % cid

    data2 = scrapertools.cachePage(pageurl, headers=headers)
    if (DEBUG): logger.info("data2="+data2)

    '''
<script type="text/javascript">
var token = "";
$.getJSON("http://myhdcast.com/file.php?id=1422998093", function(json){
	token = json.token;
	setStream(token);
});
function setStream(token) {
	jwplayer('dplayer').setup({
		file: 'rtmp://rtmp.myhdcast.com/redirect/astr5_3p9tr2nh',
		width: '653',
		height: '410',
		abouttext: 'myhdcast.com',
		aboutlink: 'http://myhdcast.com',
		skin: 'five',
		image: 'http://oi60.tinypic.com/214c94j.jpg',
		fallback: 'false',
		autostart: 'true',
		repeat: 'true',
		stretching: 'exactfit',
		primary: 'flash',
   		logo: {
        	hide: 'false',
        	file: '',
        	position: 'top-right'
    			},
		rtmp: {
			bufferlength: 3,
			securetoken: token
			},
		ga: {}
		});
		jwplayer("dplayer").onError(function() {
			//jwplayer("dplayer").play();
		});
}
</script>
    '''

    tokenurl = scrapertools.find_single_match (data2, 'getJSON\(["\']([^"\']+)')
    data3 = scrapertools.cache_page(tokenurl,headers=headers)
    if (DEBUG): logger.info("data3="+data3)
    tokenvalue = scrapertools.find_single_match (data3, '["\']token["\']\s*:\s*["\']([^"\']+)')

    rtmpurl = scrapertools.find_single_match (data2, 'file:\s*["\']([^"\']+)')

    swfurl = 'http://cdn.zerocast.tv/player/jwplayer.flash.swf'

    url = '%s swfUrl=%s swfVfy=1 live=true timeout=15 token=%s pageUrl=%s' % (rtmpurl, swfurl, tokenvalue, pageurl)

    return url
