import re

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

def request_text(url: str, fakeuser:bool=False) -> str:
    """
    Retrieves the content of the url, giving a blank string on failure.
    :param url: Location
    :param fakeuser: Set to True to use a fake user agent
    :return: Content of page or empty string
    """

    if settings.DEBUG:
        cached = {
            'https://www.rfa.org/vietnamese/audio/': './gradio/samples/rfa.html',
            'http://vi.rfi.fr/': 'gradio/samples/rfi.html',
            'https://www.voatiengviet.com/p/3864.html': './gradio/samples/voa.html',
        }
        if url in cached:
            with open(cached[url], 'r', encoding='utf-8') as f:
                return f.read()


    r = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        } if fakeuser else None,
    )
    if not r.ok:
        return ""
    return r.text


def latest_rfa():
    p = re.compile(
        'https://streamer1\.rfaweb\.org/stream/VIE/VIE-(?P<year>\d+?)-(?P<month>\d\d)(?P<day>\d\d)-(?P<hour>\d\d)(?P<minute>\d\d)\.mp3')
    text = request_text('https://www.rfa.org/vietnamese/audio/')
    tracks = []
    i = 0
    for m in p.finditer(text):
        tracks.append({
            'name': 'RFA%d' % i,
            'url': m.group()
        })
        i += 1
        if i >= 2:
            break
    return tracks


def latest_rfi():
    p = re.compile(
        'http://telechargement\.rfi\.fr/rfi/vietnamien/audio/magazines/r001/(?P<hour>\d+?)h(?P<minute>\d+?)_-_(?P<endhour>\d+?)h(?P<endminute>\d+?)_gmt_(?P<year>\d+?)(?P<month>\d\d)(?P<day>\d\d).mp3')
    text = request_text('http://vi.rfi.fr/', fakeuser=True)
    tracks = []
    i = 0
    for m in p.finditer(text):
        tracks.append({
            'name': 'RFI%d' % i,
            'url': m.group()
        })
        i += 1
        if i >= 2:
            break
    return tracks


def latest_voa():
    p = re.compile(
        'https://av\.voanews\.com/clips/VVI/(?P<year>\d+?)/(?P<month>\d\d)/(?P<day>\d\d)/\d+?-(?P<hour>\d\d)(?P<minute>\d\d)(?P<second>\d\d)-[\w\d]+?-program\.mp3')
    text = request_text('https://www.voatiengviet.com/p/3864.html')
    tracks = []
    i = 0
    for m in p.finditer(text):
        tracks.append({
            'name': 'VOA%d' % i,
            'url': m.group()
        })
        i += 1
        if i >= 2:
            break
    return tracks


def latest(request) -> HttpResponse:
    """
    Latest Broadcasts
    """
    context = {
        'sources': [
            {
                'id': 'rfa',
                'name': 'Radio Free Asia',
                'img': 'gradio/img/rfa.png',
                'tracks': latest_rfa(),
            },
            {
                'id': 'rfi',
                'name': 'Radio France Internationale',
                'img': 'gradio/img/rfi.png',
                'tracks': latest_rfi(),
            },
            {
                'id': 'voa',
                'name': 'Voice of America',
                'img': 'gradio/img/voa.png',
                'tracks': latest_voa(),
            },
        ],
    }
    return render(request, 'gradio/latest.html', context)
