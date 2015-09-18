# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para kingcast
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[kingcast.py] find_url_play")

    '''
<script type="text/javascript" src="http://www.kingcast.tv/channel.php?file=3076&width=700&height=440&autostart=true"></script>
    '''

    cid = scrapertools.find_single_match (data, '["\']http://www.kingcast.tv/channel.php\?file=([^&]+)')
    if cid == '':
        return ''
    pageurl = 'http://www.kingcast.tv/embed.php?a=' + cid

    data2 = scrapertools.cachePage(pageurl, headers=headers)
    if (DEBUG): logger.info("data2="+data2)

    '''
<script type="text/javascript" src="/jwplayer/jwplayer.js"></script>
<script>jwplayer.key="5XXb+w0txH2+cnkwOtAOWXU39zFQbZ6VT9mOA6R83tk="</script>

<script type="text/javascript" src="/content/js/player.js"></script>



<div id="player_div">
<div class="player_div" align="center">
            <span>
<div id="player"></div>
<script type='text/javascript'>
var rand = Math.floor(Math.random()*1000000000);
jwplayer('player').setup({
file: 'rtmp://91.235.143.111/live/by929jlnj',
width: '',
height: '',
image: '',
autostart: 'true',
primary: 'flash',
advertising: {
      client: "googima",
    admessage:"For more Live Channel please go to http://kingcast.tv.",
      schedule:{
                    adbreak1: {
                        offset:'pre',
                        tag: "http://delivery.vidible.tv/placement/vast/5176d880e4b082c657f08a4a/53cb8a03e4b051219735f7f6?bcid=5176c647e4b09e5e67af5b27"+rand
                    },
   
                      adbreak2: {
                        offset:'pre',
                        tag: "http://delivery.vidible.tv/placement/vast/5176d880e4b082c657f08a4a/53cb8a03e4b051219735f7f6?bcid=5176c647e4b09e5e67af5b27"+rand
                       
                    },
                    adbreak3: {
                        offset:'pre',
                        tag: "http://delivery.vidible.tv/placement/vast/5176d880e4b082c657f08a4a/53cb8a03e4b051219735f7f6?bcid=5176c647e4b09e5e67af5b27"+rand
                    },
                    adbreak4: {
                        offset:'post',
                        tag: "http://delivery.vidible.tv/placement/vast/5176d880e4b082c657f08a4a/53cb8a03e4b051219735f7f6?bcid=5176c647e4b09e5e67af5b27"+rand
        }
                }
            }
        });
 
    </script>
<!--<script type="text/javascript">
jwplayer("player").setup({
file: 'rtmp://91.235.143.111/live/by929jlnj',
image: "",
width: "",
height: "",
autostart: "true",
primary: "flash"
});
</script>-->
    '''

    rtmpurl = scrapertools.find_single_match (data2, "file:\s*['\"]([^'\"]*)")

    swfurl = 'http://www.kingcast.tv/jwplayer/jwplayer.flash.swf'

    url = '%s swfUrl=%s swfVfy=1 live=1 timeout=15 pageUrl=%s' % (rtmpurl, swfurl, pageurl)

    return url
