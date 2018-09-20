import re
import time
from datetime import datetime, timedelta
import os
import asyncio

import requests
from pyquery import PyQuery as pq
import aiofiles

from utils.helper import get_words_meaning
from configure import Config

since = datetime.strptime(Config.date_conf()['since'], "%Y%m%d")
until = since + timedelta(days=Config.date_conf()['until'])


article = {
    'title': '',
    'content': []
}
my_voices_dir = Config().out_path().get('my', 'output_voice')
host_voices_dir = Config().out_path().get('host', 'output_voice')
output_notes = Config().out_path().get('notes', 'output_notes')

# 確保檔案目錄已經存在
for path in [my_voices_dir, host_voices_dir, output_notes]:
    if not os.path.exists(os.path.abspath(output_notes)):
        os.mkdir(os.path.abspath(output_notes))

login = 'https://tw.voicetube.com/login?apilang=zh_tw&next=/&mtc=vt_web_home_header_signin&ref=vt_web_home_header_signin'
headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

async def get_everyday_page(con=None, day_format='', headers={}, cookies={}):
    return con.get(
        'https://tw.voicetube.com/everyday/{0}'.format(day_format),
        headers=headers,
        cookies=cookies
    )

async def generate_note(con=None, day_format='', headers={}, cookies={}):
    response = await get_everyday_page(
        con=same_con,
        day_format=day_format,
        headers=headers,
        cookies=cookies
    )
    if hasattr(response, 'status_code') and response.status_code == 200:
        origin_text = response.text
        doc = pq(origin_text)
        # 下載自己的錄音
        my_record = doc('#user-audio-record-player').children().attr('src')
        if my_record:
            print('開始下載個人錄音:{0},{1}'.format(day_format, my_record))
            response = requests.get(my_record)
            if hasattr(response, 'status_code') and response.status_code == 200:
                personal_voice = '{0}/{1}口說挑戰.mp3'.format(my_voices_dir, day_format)
                async with aiofiles.open(personal_voice, mode='wb') as f:
                    await f.write(response.content)
        # 內文
        article['content'] = [] # 重新指派空陣列
        for e in doc('div').filter('.video-element-width'):
            article['title'] = pq(e)('div').filter('.sm-text-size')('a').text()
            for content in pq(e)('div').filter('.text-size'):
                article['content'].append(pq(content).text())

        # 下載主人持的姓名和錄音
        div = doc('div').filter('#host-audio-scope')
        # 主持人姓名和錄音
        host_name = div('span').filter('.text-size')('a')('span').text()
        host_record = div('div').filter('.audio-player')('audio')('source').attr('src')
        host_question = div('div').filter('.sm-text-size').text()
        if host_record:
            print('開始下載主持人錄音:{0}'.format(day_format))
            response = requests.get(host_record)
            if hasattr(response, 'status_code') and response.status_code == 200:
                host_voice = '{0}/{1}({2})口說挑戰.mp3'.format(host_voices_dir, day_format, host_name)
                async with aiofiles.open(host_voice, mode='wb') as f:
                    await f.write(response.content)

            # 產生筆記
            print('開始產生筆記:{0}'.format(day_format))
            note_name = '{0}/vt{1}.md'.format(output_notes, day_format)
            with open(note_name, 'w', encoding='utf8') as file:
                file.write('# Topic\n\n')
                file.write('> {0} <br>\n'.format(article['title']))
                file.write('> {0} <br>\n'.format(article['content'][0]))
                file.write('> {0} <br>\n\n'.format(article['content'][1]))
                file.write('## Host\n')
                file.write('Host: {0} \n<br>'.format(host_name))
                file.write('Today issue: {0}\n'.format(host_question))
                file.write('<br><br>\n')
                file.write('## learning points\n')
                word_number = 1
                for words in get_words_meaning(doc):
                    file.write('{0}. _\n'.format(word_number))
                    word_number += 1
                    for w in words:
                        file.write('\t* {0}\n'.format(w))

# 使用者登入
same_con = requests.Session()
response = same_con.post(login, headers=headers, data=Config.get_conf())
if response:
    cookies = {
        'accessToken': response.cookies.get('accessToken'),
        'refreshToken': response.cookies.get('refreshToken'),
        'userToken': response.cookies.get('userToken')
    }
    cookies.update(Config.other_cookie())
    diff_days = abs((since - until).days) if abs((since - until).days) else 1

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*[
        generate_note(
            con=same_con,
            day_format=(since + timedelta(days=day)).strftime('%Y%m%d'),
            headers=headers,
            cookies=cookies
        ) for day in range(diff_days)
    ]))
    loop.close()