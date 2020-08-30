# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import datetime
import urllib
import requests
import json

#fix for datatetime.strptime returns None
class proxydt(datetime.datetime):
    @staticmethod
    def strptime(date_string, format):
        import time
        return datetime.datetime(*(time.strptime(date_string, format)[0:6]))

datetime.datetime = proxydt

#Import select name channel and epg date, time
name = xbmc.getInfoLabel('ListItem.ChannelName').replace("HD", "").replace("FHD", "").replace("hd", "").replace(" ", "").replace("*", "").replace("Č", "C").replace("Ť", "T").replace("í", "i").replace(".", "").lower()
data = requests.get("https://1url.cz/NzlOD").json()

#final url stream and check channel support
try:
    print(data[name])
except KeyError:
    dialog = xbmcgui.Dialog()
    ok = dialog.ok(xbmc.getInfoLabel('ListItem.ChannelName').replace("*", ""), "Stanice momentálně nepodporuje archiv.")
    exit()

if data[name]['check'] == name:
    epgdatetime = datetime.datetime.strptime(xbmc.getInfoLabel('ListItem.Date'), "%d.%m.%Y %H:%M") + (datetime.timedelta(hours=-2))
    stream = data['server']['1'] + data[name]['server'] + data[name]['quality'] + data[name]['catalog'] + epgdatetime.strftime("%Y%m%d") + "_" + data[name]['channel'] + "_" + epgdatetime.strftime("%Y%m%d_%H%M%S") + data[name]['url']
    code = urllib.urlopen(stream).getcode()
else:
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('Kodi', "Chyba ověření na straně serveru. Kontaktujte prosím autora doplňku.")
    exit()
    
#check stream available, play stream and add info tag
if str(code).startswith('2') or str(code).startswith('3') :
    namechannel = xbmc.getInfoLabel('ListItem.ChannelName').replace("*", "")
    info = {
        'Title': namechannel + ": " + xbmc.getInfoLabel('Listitem.Title') + " (Archiv)",
        'year': xbmc.getInfoLabel('ListItem.Year'),
        'genre': xbmc.getInfoLabel('ListItem.Genre'),
        'plot': xbmc.getInfoLabel('ListItem.Plot'),
        'media-type': 'tvshow',
    }
    image = {
        'thumb': xbmc.getInfoLabel('Listitem.Icon'),
        'icon': xbmc.getInfoLabel('Listitem.Icon'),
    }
    item = xbmcgui.ListItem()
    item.setInfo('video', info)
    item.setArt(image)
    xbmc.Player().play(stream, item)
else:
    dialog = xbmcgui.Dialog()
    ok = dialog.ok(xbmc.getInfoLabel('ListItem.ChannelName').replace("*", ""), "Pořad není momentálně v archivu dostupný.")
    exit ()