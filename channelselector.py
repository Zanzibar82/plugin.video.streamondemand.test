# -*- coding: utf-8 -*-
import urlparse,urllib2,urllib,re
import os
import sys
from core import config
from core import logger
from core.item import Item

DEBUG = True
CHANNELNAME = "channelselector"

def getmainlist(preferred_thumb=""):
    logger.info("channelselector.getmainlist")
    itemlist = []

    # Obtiene el idioma, y el literal
    idioma = config.get_setting("languagefilter")
    logger.info("channelselector.getmainlist idioma=%s" % idioma)
    langlistv = [config.get_localized_string(30025),config.get_localized_string(30026),config.get_localized_string(30027),config.get_localized_string(30028),config.get_localized_string(30029)]
    try:
        idiomav = langlistv[int(idioma)]
    except:
        idiomav = langlistv[0]

    # Añade los canales que forman el menú principal
    itemlist.append( Item(title=config.get_localized_string(30118) , channel="channelselector" , action="channeltypes", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales.png") ) )
    #itemlist.append( Item(title=config.get_localized_string(30130) , channel="novedades" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_novedades.png") ) )
    #itemlist.append( Item(title="Contenuti Vari" , channel="novedades" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_novedades.png") ) )
    itemlist.append( Item(title="Sport" , channel="sports-main" , action="mainlist", thumbnail = "https://raw.githubusercontent.com/Zanzibar82/images/master/posters/sports-main.png" ) )
    #itemlist.append( Item(title=config.get_localized_string(30103) , channel="buscador" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_buscar.png")) )
    itemlist.append( Item(title="Ricerca Globale" , channel="buscador" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_buscar.png")) )
    itemlist.append( Item(title="Oggi in TV" , channel="filmontv" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_filmontv.png")) )
    itemlist.append( Item(title=config.get_localized_string(40103) , channel="youtube" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_youtube.png")) )
    #if config.is_xbmc(): itemlist.append( Item(title=config.get_localized_string(30128) , channel="trailertools" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_trailers.png")) )
    itemlist.append( Item(title=config.get_localized_string(30102) , channel="favoritos" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_favoritos.png")) )
    #itemlist.append( Item(title=config.get_localized_string(30131) , channel="libreria" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_biblioteca.png")) )
    if config.get_platform()=="rss":itemlist.append( Item(title="pyLOAD (Beta)" , channel="pyload" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"pyload.png")) )
    itemlist.append( Item(title=config.get_localized_string(30101) , channel="descargas" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_descargas.png")) )

    if "xbmceden" in config.get_platform():
        itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_configuracion.png"), folder=False) )
    else:
        itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_configuracion.png")) )

    #if config.get_setting("fileniumpremium")=="true":
    #   itemlist.append( Item(title="Torrents (Filenium)" , channel="descargasfilenium" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(),"torrents.png")) )

    #if config.get_library_support():
    if config.get_platform()!="rss": itemlist.append( Item(title=config.get_localized_string(30104) , channel="ayuda" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_ayuda.png")) )
    return itemlist

# TODO: (3.1) Pasar el código específico de XBMC al laucher
def mainlist(params,url,category):
    logger.info("channelselector.mainlist")

    # Verifica actualizaciones solo en el primer nivel
    if config.get_platform()!="boxee":
        try:
            from core import updater
        except ImportError:
            logger.info("channelselector.mainlist No disponible modulo actualizaciones")
        else:
            if config.get_setting("updatecheck2") == "true":
                logger.info("channelselector.mainlist Verificar actualizaciones activado")
                try:
                    updater.checkforupdates()
                except:
                    import xbmcgui
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Impossibile connettersi","Non è stato possibile verificare","la disponibilità di aggiornamenti")
                    logger.info("channelselector.mainlist Fallo al verificar la actualización")
                    pass
            else:
                logger.info("channelselector.mainlist Verificar actualizaciones desactivado")

    itemlist = getmainlist()
    for elemento in itemlist:
        logger.info("channelselector.mainlist item="+elemento.title)
        addfolder(elemento.title , elemento.channel , elemento.action , thumbnail=elemento.thumbnail, folder=elemento.folder)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def getchanneltypes(preferred_thumb=""):
    logger.info("channelselector getchanneltypes")
    itemlist = []
    itemlist.append( Item( title=config.get_localized_string(30121) , channel="channelselector" , action="listchannels" , category="*"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_todos.png")))
    itemlist.append( Item( title="Top Channels" , channel="channelselector" , action="listchannels" , category="B"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_topchannels.png")))
    itemlist.append( Item( title=config.get_localized_string(30122) , channel="channelselector" , action="listchannels" , category="F"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_peliculas.png")))
    itemlist.append( Item( title=config.get_localized_string(30123) , channel="channelselector" , action="listchannels" , category="S"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_series.png")))
    itemlist.append( Item( title=config.get_localized_string(30124) , channel="channelselector" , action="listchannels" , category="A"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_anime.png")))
    itemlist.append( Item( title=config.get_localized_string(30125) , channel="channelselector" , action="listchannels" , category="D"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_documentales.png")))
    itemlist.append( Item( title=config.get_localized_string(30136) , channel="channelselector" , action="listchannels" , category="VOS" , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_vos.png")))
    #itemlist.append( Item( title=config.get_localized_string(30126) , channel="channelselector" , action="listchannels" , category="M"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_musica.png")))
    #itemlist.append( Item( title="Bittorrent" , channel="channelselector" , action="listchannels" , category="T"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_torrent.png")))
    #itemlist.append( Item( title=config.get_localized_string(30127) , channel="channelselector" , action="listchannels" , category="L"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_latino.png")))
    #if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title=config.get_localized_string(30126) , channel="channelselector" , action="listchannels" , category="X"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_adultos.png")))
    #itemlist.append( Item( title=config.get_localized_string(30127) , channel="channelselector" , action="listchannels" , category="G"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_servidores.png")))
    #itemlist.append( Item( title=config.get_localized_string(30134) , channel="channelselector" , action="listchannels" , category="NEW" , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"novedades.png")))
    return itemlist
   
def channeltypes(params,url,category):
    logger.info("channelselector.mainlist channeltypes")

    lista = getchanneltypes()
    for item in lista:
        addfolder(item.title,item.channel,item.action,item.category,item.thumbnail,item.thumbnail)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def listchannels(params,url,category):
    logger.info("channelselector.listchannels")

    lista = filterchannels(category)
    for channel in lista:
        if channel.type=="xbmc" or channel.type=="generic":
            if channel.channel=="personal":
                thumbnail=config.get_setting("personalchannellogo")
            elif channel.channel=="personal2":
                thumbnail=config.get_setting("personalchannellogo2")
            elif channel.channel=="personal3":
                thumbnail=config.get_setting("personalchannellogo3")
            elif channel.channel=="personal4":
                thumbnail=config.get_setting("personalchannellogo4")
            elif channel.channel=="personal5":
                thumbnail=config.get_setting("personalchannellogo5")
            else:
                thumbnail=channel.thumbnail
                if thumbnail == "":
                    thumbnail=urlparse.urljoin(get_thumbnail_path(),channel.channel+".png")
            addfolder(channel.title , channel.channel , "mainlist" , channel.channel, thumbnail = thumbnail)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def filterchannels(category,preferred_thumb=""):
    returnlist = []

    if category=="NEW":
        channelslist = channels_history_list()
        for channel in channelslist:
            channel.thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),channel.channel+".png")
            channel.plot = channel.category.replace("VOS","Versione con audio originale e sottotitoli").replace("F","Film").replace("S","Serie TV").replace("D","Documentari").replace("A","Anime").replace("B","Best").replace(",",", ")
            returnlist.append(channel)
    else:
        try:
            idioma = config.get_setting("languagefilter")
            logger.info("channelselector.filterchannels idioma=%s" % idioma)
            langlistv = ["","ES","EN","IT","PT"]
            idiomav = langlistv[int(idioma)]
            logger.info("channelselector.filterchannels idiomav=%s" % idiomav)
        except:
            idiomav=""

        channelslist = channels_list()
   
        for channel in channelslist:
            # Pasa si no ha elegido "todos" y no está en la categoría elegida
            if category<>"*" and category not in channel.category:
                #logger.info(channel[0]+" no entra por tipo #"+channel[4]+"#, el usuario ha elegido #"+category+"#")
                continue
            # Pasa si no ha elegido "todos" y no está en el idioma elegido
            if channel.language<>"" and idiomav<>"" and idiomav not in channel.language:
                #logger.info(channel[0]+" no entra por idioma #"+channel[3]+"#, el usuario ha elegido #"+idiomav+"#")
                continue
            if channel.thumbnail == "":
                channel.thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),channel.channel+".png")
            channel.plot = channel.category.replace("VOS","Versione con audio originale e sottotitoli").replace("F","Film").replace("S","Serie TV").replace("D","Documentari").replace("A","Anime").replace("B","Best").replace(",",", ")
            returnlist.append(channel)

    return returnlist

def channels_history_list():
    itemlist = []
    return itemlist

def channels_list():
    itemlist = []

    #itemlist.append( Item( viewmode="movie", title="Inserisci un URL"         , channel="tengourl"   , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname") , channel="personal" , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel2")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname2") , channel="personal2" , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel3")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname3") , channel="personal3" , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel4")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname4") , channel="personal4" , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel5")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname5") , channel="personal5" , language="" , category="" , type="generic"  ))
    itemlist.append( Item( title="[COLOR azure]AltaDefinizione01[/COLOR]"      , channel="altadefinizione01"           , language="IT"    , category="B,F,S,A"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Altadefinizione.click[/COLOR]" , channel="altadefinizioneclick" , language="IT" , category="F,S,A" , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Anime Sub Ita[/COLOR]"   , channel="animesubita"           , language="IT"    , category="A"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Asian Sub-Ita[/COLOR]"      , channel="asiansubita"           , language="IT"    , category="F,S"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Casa-Cinema[/COLOR]"         , channel="casacinema"           , language="IT"    , category="F,S,A,VOS"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]CineBlog 01[/COLOR]"         , channel="cineblog01"           , language="IT"    , category="B,F,S,A,VOS"   , type="generic"  ))
    #itemlist.append( Item( title="[COLOR azure]CineBlog01.FM[/COLOR]"       , channel="cineblogfm"           , language="IT"    , category="F,S"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Cinemagratis[/COLOR]"        , channel="cinemagratis"       , language="IT"    , category="F"       , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Cucinarefacile[/COLOR]"        , channel="cucinarefacile"       , language="IT"    , category="D"       , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Darkstream[/COLOR]"        , channel="darkstream"       , language="IT"    , category="B,F"       , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Documentari Streaming[/COLOR]"  , channel="documentaristreaming"           , language="IT"    , category="D"   , type="generic"))
    #itemlist.append( Item( title="[COLOR azure]Documoo[/COLOR]"      , channel="documoo"           , language="IT"    , category="D"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Eurostreaming[/COLOR]"       , channel="eurostreaming"           , language="IT"    , category="F,S"    , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Fastvideo.tv[/COLOR]"        , channel="fastvideotv"       , language="IT"    , category="B,F"       , type="generic"))
    itemlist.append( Item( title="[COLOR azure]FilmGratis.cc[/COLOR]"       , channel="filmgratiscc"           , language="IT"    , category="F"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]FilmStream.org[/COLOR]"          , channel="filmstream"           , language="IT"    , category="F,S"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]FilmStream.to[/COLOR]"       , channel="filmstreampw"           , language="IT"    , category="F,S"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Film per tutti[/COLOR]"      , channel="filmpertutti"           , language="IT"    , category="F,S,A"    , type="generic"     ))
    itemlist.append( Item( title="[COLOR azure]Film Senza Limiti[/COLOR]"   , channel="filmsenzalimiti"       , language="IT"    , category="B,F"        , type="generic"     ))
    itemlist.append( Item( title="[COLOR azure]FilmSubito[/COLOR]"          , channel="filmsubitotv"           , language="IT"    , category="F,S,A"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Foxycinema[/COLOR]"          , channel="foxycinema"           , language="IT"    , category="F,S,A"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Guardaserie.net[/COLOR]"     , channel="guardaserie"       , language="IT"    , category="S,B"        , type="generic"))
    itemlist.append( Item( title="[COLOR azure]GuardareFilm[/COLOR]"         , channel="guardarefilm"           , language="IT"    , category="F,S,A"    , type="generic"))
    #itemlist.append( Item( title="[COLOR azure]Hubberfilm[/COLOR]"          , channel="hubberfilm"           , language="IT"    , category="F,S,A"   , type="generic"))
    #itemlist.append( Item( title="[COLOR azure]ildocumento.it[/COLOR]"      , channel="ildocumento"           , language="IT"    , category="D"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]ItaFilm.tv[/COLOR]"      , channel="itafilmtv"           , language="IT"    , category="F,S,A,D"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Italia-Film.co[/COLOR]"      , channel="italiafilm"           , language="IT"    , category="F,S,A"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Italian-Stream [/COLOR]"        , channel="italianstream"       , language="IT"    , category="F,S"       , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Italia Serie[/COLOR]"        , channel="italiaserie"           , language="IT"    , category="F,S,A"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]ItaStreaming[/COLOR]"      , channel="itastreaming" , language="IT" , category="F,S,A" , type="generic"))
    itemlist.append( Item( title="[COLOR azure]LiberoITA[/COLOR]"       , channel="liberoita"           , language="IT"    , category="F,S,A"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Liberostreaming[/COLOR]" , channel="liberostreaming" , language="IT" , category="F,S,A" , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Pianeta Streaming[/COLOR]"   , channel="pianetastreaming"           , language="IT"    , category="F,S,A"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Pirate Streaming[/COLOR]"    , channel="piratestreaming"           , language="IT"    , category="F,S,A"   , type="generic"  ))
    itemlist.append( Item( title="[COLOR azure]PortaleHD[/COLOR]"   , channel="portalehd"           , language="IT"    , category="F,S,A,B"   , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Serie HD[/COLOR]"     , channel="seriehd"       , language="IT"    , category="S"        , type="generic"))
    itemlist.append( Item( title="[COLOR azure]Serie TV Sub ITA[/COLOR]"    , channel="serietvsubita"         , language="IT" , category="S"        , type="generic" , extra="Series"))
    itemlist.append( Item( title="[COLOR azure]StreamBlog[/COLOR]"    , channel="streamblog"         , language="IT" , category="S,F,A"        , type="generic" , extra="Series"))
    itemlist.append( Item( title="[COLOR azure]Streaming01[/COLOR]"    , channel="streaming01"         , language="IT" , category="B,F"        , type="generic" , extra="Series"))
    itemlist.append( Item( title="[COLOR azure]Streaminfilmit[/COLOR]"    , channel="streamingfilmit"         , language="IT" , category="F"        , type="generic" , extra="Series"))
    itemlist.append( Item( title="[COLOR azure]Tantifilm[/COLOR]"        , channel="tantifilm"       , language="IT"    , category="B,F"       , type="generic"))

    return itemlist

def addfolder(nombre,channelname,accion,category="",thumbnailname="",thumbnail="",folder=True):
    if category == "":
        try:
            category = unicode( nombre, "utf-8" ).encode("iso-8859-1")
        except:
            pass
   
    import xbmc
    import xbmcgui
    import xbmcplugin
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , category )
    xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=folder)

def get_thumbnail_path(preferred_thumb=""):

    WEB_PATH = ""
   
    if preferred_thumb=="":
        thumbnail_type = config.get_setting("thumbnail_type")
        if thumbnail_type=="":
            thumbnail_type="2"
       
        if thumbnail_type=="0":
            WEB_PATH = "https://raw.githubusercontent.com/Zanzibar82/images/master/posters/"
        elif thumbnail_type=="1":
            WEB_PATH = "https://raw.githubusercontent.com/Zanzibar82/images/master/banners/"
        elif thumbnail_type=="2":
            WEB_PATH = "https://raw.githubusercontent.com/Zanzibar82/images/master/squares/"
    else:
        WEB_PATH = "https://raw.githubusercontent.com/Zanzibar82/images/master/"+preferred_thumb+"/"

    return WEB_PATH
