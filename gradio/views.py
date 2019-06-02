import re

import datetime
from typing import Dict, List

import pytz
import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.timezone import localtime


def pretty_datetime(dt: datetime.datetime) -> str:
    ext = 'th'
    exts = {
        0: 'st',
        1: 'nd',
        3: 'rd',
    }
    ones = dt.day % 10
    if not (11 <= dt.day <= 13) and ones in exts:
        ext = exts[ones]

    # return '{dt.day}{ext} {dt:%b} {dt.hour}:{dt:%M}'.format(dt=dt, ext=ext)
    return '{dt.day}{ext} {dt:%H}:{dt:%M}'.format(dt=dt, ext=ext)

def request_text(url: str) -> str:
    """
    Retrieves the content of the url, giving a blank string on failure.
    :param url: Location
    :param fakeuser: Set to True to use a fake user agent
    :return: Content of page or empty string
    """

    if False and settings.DEBUG:
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
        },
    )
    if not r.ok:
        return ""
    return r.text

def retrieve_latest(url:str, pattern:str) -> List[Dict]:
    text = request_text(url)
    p = re.compile(pattern)
    tracks = []
    i = 0
    for m in p.finditer(text):
        groups = m.groupdict()
        dateutc = datetime.datetime(int(groups['year']), int(groups['month']), int(groups['day']), int(groups['hour']), int(groups['minute']), tzinfo=datetime.timezone.utc)
        datelocal = localtime(dateutc)
        tracks.append({
            'name': pretty_datetime(datelocal),
            'datetime': datelocal,
            'url': m.group()
        })
        i += 1
        if i >= 2:
            break
    tracks.sort(key=lambda x: x['datetime'], reverse=True)
    return tracks

def latest(request) -> HttpResponse:
    """
    Latest Broadcasts
    """
    smtv = {
        'id': 'smtv',
        'name': 'Supreme Master TV',
        'img': 'gradio/img/smtv.png',
        'tracks': [{
            'name': 'Live',
            'datetime': localtime(datetime.datetime.now(tz=datetime.timezone.utc)),
            'url': 'https://smtv.vo.llnwd.net/wse_us1/audio.m3u8',
            'stream': True
        }]
    }
    rfa = {
        'id': 'rfa',
        'name': 'Radio Free Asia',
        'img': 'gradio/img/rfa.png',
        'tracks': retrieve_latest(
            'https://www.rfa.org/vietnamese/audio/',
            'https://streamer1\.rfaweb\.org/stream/VIE/VIE-(?P<year>\d+?)-(?P<month>\d\d)(?P<day>\d\d)-(?P<hour>\d\d)(?P<minute>\d\d)\.mp3',
        ),
    }
    rfi = {
        'id': 'rfi',
        'name': 'Radio France Internationale',
        'img': 'gradio/img/rfi.png',
        'tracks': retrieve_latest(
            'http://vi.rfi.fr/',
            'http://telechargement\.rfi\.fr/rfi/vietnamien/audio/magazines/r001/(?P<hour>\d+?)h(?P<minute>\d+?)_-_(?P<endhour>\d+?)h(?P<endminute>\d+?)_gmt_(?P<year>\d+?)(?P<month>\d\d)(?P<day>\d\d).mp3',
        ),
    }
    voa = {
        'id': 'voa',
        'name': 'Voice of America',
        'img': 'gradio/img/voa.png',
        'tracks': retrieve_latest(
            'https://www.voatiengviet.com/p/3864.html',
            'https://av\.voanews\.com/clips/VVI/(?P<year>\d+?)/(?P<month>\d\d)/(?P<day>\d\d)/\d+?-(?P<hour>\d\d)(?P<minute>\d\d)(?P<second>\d\d)-[\w\d]+?-program\.mp3',
        ),
    }
    context = {
        'sources': [
            rfa,
            rfi,
            voa,
            smtv
        ],
    }
    return render(request, 'gradio/latest.html', context)
