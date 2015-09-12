# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector for openload.io
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# by DrZ3r0
# ------------------------------------------------------------

import re

from core import scrapertools
from core import logger

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Connection', 'keep-alive']
]


def test_video_exists(page_url):
    logger.info("[openload.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url, headers=headers)

    if 'We are sorry!' in data:
        return False, 'File Not Found or Removed.'

    return True, ""


def __decode_O(html):
    match = re.search('>\s*(eval\(function.*?)</script>', html, re.DOTALL)
    if match:
        from lib.jsbeautifier.unpackers import packer
        html = packer.unpack(match.group(1))
        html = html.replace('\\\\', '\\')

    match = re.search('(l=.*?)(?:$|</script>)', html, re.DOTALL)
    if match:
        s = match.group(1)

        O = {
            '___': 0,
            '$$$$': "f",
            '__$': 1,
            '$_$_': "a",
            '_$_': 2,
            '$_$$': "b",
            '$$_$': "d",
            '_$$': 3,
            '$$$_': "e",
            '$__': 4,
            '$_$': 5,
            '$$__': "c",
            '$$_': 6,
            '$$$': 7,
            '$___': 8,
            '$__$': 9,
            '$_': "constructor",
            '$$': "return",
            '_$': "o",
            '_': "u",
            '__': "t",
        }
        match = re.search('l\.\$\(l\.\$\((.*?)\)\(\)\)\(\);', s)
        if match:
            s1 = match.group(1)
            s1 = s1.replace(' ', '')
            s1 = s1.replace('(![]+"")', 'false')
            s3 = ''
            for s2 in s1.split('+'):
                if s2.startswith('l.'):
                    s3 += str(O[s2[2:]])
                elif '[' in s2 and ']' in s2:
                    key = s2[s2.find('[') + 3:-1]
                    s3 += s2[O[key]]
                else:
                    s3 += s2[1:-1]

            s3 = s3.replace('\\\\', '\\')
            s3 = s3.decode('unicode_escape')
            s3 = s3.replace('\\/', '/')
            s3 = s3.replace('\\\\"', '"')
            s3 = s3.replace('\\"', '"')

            print s3

            match = re.search(r'attr\("href",\s*"([^"]+)"', s3)
            if match:
                return match.group(1)


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[openload.py] url=" + page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url, headers=headers)

    # URL del vídeo
    url = __decode_O(data)
    video_urls.append([".mp4" + " [Openload]", url])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    patronvideos = '//(?:www.)?openload.../(?:embed|f)/([0-9a-zA-Z-_]+)'
    logger.info("[openload.py] find_videos #" + patronvideos + "#")

    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for media_id in matches:
        titulo = "[Openload]"
        url = 'http://openload.co/f/%s' % media_id
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'openload'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
