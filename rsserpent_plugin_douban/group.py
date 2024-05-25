from typing import Any, Dict

import arrow
from pyquery import PyQuery
from rsserpent_rev.utils import HTTPClient, cached


path = "/douban/group/{gid}"


def timeHandler(t):
    # 02-16 13:21
    if t.find(':') != -1:
        year = arrow.now('Asia/Shanghai').year
        t = f'{year}-{t}'
    # 2021-12-22
    else:
        t = f'{t} 00:00'
    return arrow.get(t, tzinfo='Asia/Shanghai').to('+00:00')


@cached
async def provider(gid: str) -> Dict[str, Any]:
    """订阅小组讨论。"""
    url = f'https://www.douban.com/group/{gid}/discussion'
    headers = {
        'Host': 'www.douban.com',
        'Referer': 'https://www.douban.com/group/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    async with HTTPClient() as client:
        response = await client.get(url, headers=headers)
    dom = PyQuery(response.text)
    author = dom("title").text().strip()
    dom("div#content tr span.pl").parents("tr").remove()
    items = dom("div#content tr").not_('.th').items()
    return {
        "title": f"{author}的讨论",
        "link": f"https://www.douban.com/group/{gid}/",
        "description": f"{author}的讨论",
        "items": [
            {
                "title": f'[{item("td.r-count").text()}回复]{item("td.title > a").attr("title").split("?")[0]}',
                "description": '',
                "link": item("td.title > a").attr('href').replace('www', 'm'),
                "pub_date": timeHandler(item("td.time").text()),
                "author": author,
            }
            for item in items
        ],
    }
