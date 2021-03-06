# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para piratestreaming
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import urlparse
import re
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "filmstream"
__category__ = "F"
__type__ = "generic"
__title__ = "Film-stream.org (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://film-stream.org"


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.filmstream mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Ultimi Film Inseriti[/COLOR]",
                     action="peliculas",
                     url=host,
                     thumbnail="http://dc584.4shared.com/img/XImgcB94/s7/13feaf0b538/saquinho_de_pipoca_01"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film Per Genere[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     extra="serie",
                     action="peliculas",
                     url="%s/category/serie-tv/" % host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/New%20TV%20Shows.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist


def categorias(item):
    logger.info("streamondemand.filmstream categorias")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    logger.info(data)

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data, '<ul class="sf-menu">(.*?)</ul>')

    # The categories are the options for the combo
    patron = '<a href="([^"]+)" >([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

    for url, titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url, url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot))

    return itemlist


def search(item, texto):
    logger.info("[filmstream.py] " + item.url + " search " + texto)
    item.url = "%s/?s=%s&x=0&y=0" % (host, texto)
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def peliculas(item):
    logger.info("streamondemand.filmstream peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<div class="galleryitem".*?>\s*'
    patron += '<a href="?([^>"]+)"?.*?title="?([^>"]+)"?.*?<img.*?src="([^>"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl)
        start = html.find("</strong></p>")
        end = html.find("<p>&nbsp;</p>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("Streaming", ""))
        if scrapedtitle.startswith("Permanent Link to "):
            scrapedtitle = scrapedtitle[18:]
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="episodios" if item.extra == "serie" else "findvideos",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True,
                 fanart=scrapedthumbnail))

    # Extrae el paginador
    patronvideos = '<li><a href="([^"]+)">&gt;</a></li>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas",
                 title="[COLOR orange]Successivo>>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist


# def episodios(item):
#     logger.info("streamondemand.filmstream episodios")
#
#     itemlist = []
#
#     ## Descarga la página
#     data = scrapertools.cache_page(item.url)
#     data = scrapertools.decodeHtmlentities(data)
#
#     lang_titles = []
#     starts = []
#     patron = r'<p style="text-align: center;"><strong>((?:STAGIONE|MINISERIE|SERIE)[^<]+)'
#     matches = re.compile(patron, re.IGNORECASE).finditer(data)
#     for match in matches:
#         season_title = match.group(1)
#         if season_title != '':
#             lang_titles.append('SUB ITA' if 'SUB' in season_title.upper() else 'ITA')
#             starts.append(match.end(0))
#
#     i = 1
#     len_lang_titles = len(lang_titles)
#     lang_title = lang_titles[0]
#     patron = r'<p style="text-align: center;">(.*?)(<a[^h]*href="[^"]+"[^>]*>([^<]+)</a>.+)'
#     matches = re.compile(patron).finditer(data)
#     for match in matches:
#         ## Extrae las entradas
#         if i < len_lang_titles and starts[i] < match.end(0):
#             lang_title = lang_titles[i]
#             i += 1
#         title1, data, title2 = match.group(1), match.group(2), match.group(3)
#         title1 = re.sub(r'<[^>]*>', '', title1)
#         scrapedtitle = title2 if title1 == '' else title1
#         scrapedtitle = scrapedtitle.replace('–', '').strip()
#
#         itemlist.append(
#             Item(channel=__channel__,
#                  action="findvid_serie",
#                  title="[COLOR azure]" + scrapedtitle + " (" + lang_title + ")" + "[/COLOR]",
#                  url=item.url,
#                  thumbnail=item.thumbnail,
#                  extra=data,
#                  fulltitle=item.title,
#                  show=item.title))
#
#     return itemlist


def episodios(item):
    logger.info("streamondemand.filmstream episodios")

    itemlist = []

    ## Descarga la página
    data = scrapertools.cache_page(item.url)
    data = scrapertools.decodeHtmlentities(data)

    lang_titles = []
    starts = []
    patron = r'<p(?: style="text-align: center;")?>.*?<strong>((?:STAGIONE|MINISERIE|WEBSERIE|SERIE)[^<]+)'
    matches = re.compile(patron, re.IGNORECASE).finditer(data)
    for match in matches:
        season_title = match.group(1)
        if season_title != '':
            lang_titles.append('SUB ITA' if 'SUB' in season_title.upper() else 'ITA')
            starts.append(match.end(0))

    i = 1
    len_lang_titles = len(lang_titles)

    while i <= len_lang_titles:
        inizio = starts[i - 1]
        fine = starts[i] if i < len_lang_titles else -1

        html = data[inizio:fine]
        lang_title = lang_titles[i - 1]

        ep_list1(html, item, itemlist, lang_title)

        ep_list2(html, item, itemlist, lang_title)

        ep_list3(html, item, itemlist, lang_title)

        ep_list4(html, item, itemlist, lang_title)

        i += 1

    return itemlist


def ep_list1(data, item, itemlist, lang_title):
    patron = r'<p style="text-align: center;">(.*?)(<a[^h]*href="[^"]+"[^>]*>([^<]+)</a>.+)'
    matches = re.compile(patron).findall(data)
    for title1, html, title2 in matches:
        ## Extrae las entradas
        title1 = re.sub(r'<[^>]*>', '', title1)
        scrapedtitle = title2 if title1 == '' else title1
        scrapedtitle = scrapedtitle.replace('–', '').strip()

        itemlist.append(
            Item(channel=__channel__,
                 action="findvid_serie",
                 title="[COLOR azure]" + scrapedtitle + " (" + lang_title + ")" + "[/COLOR]",
                 url=item.url,
                 thumbnail=item.thumbnail,
                 extra=html,
                 fulltitle=item.title,
                 show=item.title))


def ep_list2(data, item, itemlist, lang_title):
    patron = r'<p style="text-align: center;"><strong>([^<]+)<br />'
    matches = re.compile(patron).finditer(data)
    starts = []
    scrapedtitles = []
    for match in matches:
        ## Extrae las entradas
        title = re.sub(r'<[^>]*>', '', match.group(1))
        scrapedtitles.append(title.replace('–', '').strip())
        starts.append(match.end(0))

    i = 1
    len_starts = len(starts)
    while i <= len_starts:
        inizio = starts[i - 1]
        fine = starts[i] if i < len_starts else -1

        itemlist.append(
            Item(channel=__channel__,
                 action="findvid_serie",
                 title="[COLOR azure]" + scrapedtitles[i - 1] + " (" + lang_title + ")" + "[/COLOR]",
                 url=item.url,
                 thumbnail=item.thumbnail,
                 extra=data[inizio:fine],
                 fulltitle=item.title,
                 show=item.title))
        i += 1


def ep_list3(data, item, itemlist, lang_title):
    patron = r'<p><strong>([^<]+)</strong>'
    matches = re.compile(patron).finditer(data)
    starts = []
    scrapedtitles = []
    for match in matches:
        ## Extrae las entradas
        title = re.sub(r'<[^>]*>', '', match.group(1))
        scrapedtitles.append(title.replace('–', '').strip())
        starts.append(match.end(0))

    i = 1
    len_starts = len(starts)
    while i <= len_starts:
        inizio = starts[i - 1]
        fine = starts[i] if i < len_starts else -1

        itemlist.append(
            Item(channel=__channel__,
                 action="findvid_serie",
                 title="[COLOR azure]" + scrapedtitles[i - 1] + " (" + lang_title + ")" + "[/COLOR]",
                 url=item.url,
                 thumbnail=item.thumbnail,
                 extra=data[inizio:fine],
                 fulltitle=item.title,
                 show=item.title))
        i += 1


def ep_list4(data, item, itemlist, lang_title):
    patron = r'<p>(<strong>[^<]*<strong>[^<]*</strong>[^<]*)(?:</strong>)?<br />'
    matches = re.compile(patron).finditer(data)
    starts = []
    scrapedtitles = []
    for match in matches:
        ## Extrae las entradas
        title = re.sub(r'<[^>]*>', '', match.group(1))
        scrapedtitles.append(title.replace('–', '').strip())
        starts.append(match.end(0))

    i = 1
    len_starts = len(starts)
    while i <= len_starts:
        inizio = starts[i - 1]
        fine = starts[i] if i < len_starts else -1

        itemlist.append(
            Item(channel=__channel__,
                 action="findvid_serie",
                 title="[COLOR azure]" + scrapedtitles[i - 1] + " (" + lang_title + ")" + "[/COLOR]",
                 url=item.url,
                 thumbnail=item.thumbnail,
                 extra=data[inizio:fine],
                 fulltitle=item.title,
                 show=item.title))
        i += 1


def findvid_serie(item):
    logger.info("streamondemand.filmstream findvideos")

    ## Descarga la página
    data = item.extra

    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist

