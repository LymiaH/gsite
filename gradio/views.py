import datetime
import re
from typing import Dict, List, Callable

import requests
import urllib3
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
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

    urllib3.util.connection.HAS_IPV6 = False
    r = requests.get(
        url=url,
        headers={
            'Connection': 'close',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        },
    )
    if not r.ok:
        return ""
    return r.text


def match_group_to_url(m: re.match) -> str:
    return m.group()


def retrieve_latest(url: str, pattern: str, match_to_url: Callable[[re.match], str] = match_group_to_url) -> List[Dict]:
    text = request_text(url)
    p = re.compile(pattern)
    tracks = []
    for m in p.finditer(text):
        groups = m.groupdict()
        dateutc = datetime.datetime(int(groups['year']), int(groups['month']), int(groups['day']), int(groups['hour']),
                                    int(groups['minute']), tzinfo=datetime.timezone.utc)
        datelocal = localtime(dateutc)
        tracks.append({
            'name': pretty_datetime(datelocal),
            'datetime': datelocal,
            'url': match_to_url(m),
        })
    tracks.sort(key=lambda x: x['datetime'], reverse=True)
    return tracks[:2]


def match_escaped_to_url(m: re.match) -> str:
    groups = m.groupdict()
    escaped_url = groups['escaped_url']
    return escaped_url.replace('\\/', '/')


def retrieve_rfi() -> List[Dict]:
    text = request_text('https://www.rfi.fr/vi/chương-trình')
    p = re.compile(r'\/vi(?:\/[^\/\"]+?)*?\/[^\/\"]*?(?P<year>\d\d\d\d)(?P<month>\d\d)(?P<day>\d\d)[^\/\"]+?(?P<hour>\d\d)h(?P<minute>\d\d)[^\/\"]*?\/?(?=\")')
    urls_to_check = []
    for m in p.finditer(text):
        groups = m.groupdict()
        dateutc = datetime.datetime(int(groups['year']), int(groups['month']), int(groups['day']), int(groups['hour']),
                                    int(groups['minute']), tzinfo=datetime.timezone.utc)
        datelocal = localtime(dateutc)
        urls_to_check.append({
            'datetime': datelocal,
            'url': 'https://www.rfi.fr' + m.group(),
        })
    urls_to_check.sort(key=lambda x: x['datetime'], reverse=True)
    urls_to_check = urls_to_check[:2]
    tracks = []
    for u in urls_to_check:
        temp = retrieve_latest(
            u['url'],
            r'\"contentUrl\":\"(?P<escaped_url>https:\\\/\\\/aod-rfi\.akamaized\.net\\\/rfi\\\/vietnamien\\\/audio\\\/magazines\\\/r001\\\/(?P<hour>\d+?)h(?P<minute>\d+?)_-_(?P<endhour>\d+?)h(?P<endminute>\d+?)_gmt_(?P<year>\d+?)(?P<month>\d\d)(?P<day>\d\d)\.mp3)\"',
            match_escaped_to_url,
        )
        tracks.extend(temp)
    tracks.sort(key=lambda x: x['datetime'], reverse=True)
    return tracks[:2]


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
            'url': 'https://cf-lbs.suprememastertv.com/audio.m3u8',
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
        'tracks': retrieve_rfi(),
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
