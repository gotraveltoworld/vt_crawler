import re
import time
from datetime import datetime, timedelta
import os
import json

import requests

from configure import Config

since = datetime.strptime(Config.date_conf()['since'], "%Y%m%d")
if Config.date_conf()['until']:
    until = since + timedelta(days=Config.date_conf()['until'])
else:
    until = since + timedelta(days=1)

article = {
    'title': '',
    'content': []
}
my_voices_dir = Config().out_path().get('my', 'output_voice')
host_voices_dir = Config().out_path().get('host', 'output_voice')
output_notes = Config().out_path().get('notes', 'output_notes')

# 確保檔案目錄已經存在
for path in [my_voices_dir, host_voices_dir, output_notes]:
    if not os.path.exists(os.path.abspath(path)):
        os.mkdir(os.path.abspath(path))

# 登入
login = 'https://tw.voicetube.com/login?apilang=zh_tw&next=/&mtc=vt_web_home_header_signin&ref=vt_web_home_header_signin'
headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
userId = '1352160'
platform = 'Web'
# 建立通同連線
same_con = requests.Session()
response = same_con.post(login, headers=headers, data=Config.get_conf())
if response:
    cookies = {
        'accessToken': response.cookies.get('accessToken'),
        'refreshToken': response.cookies.get('refreshToken'),
        'userToken': response.cookies.get('userToken')
    }
    cookies.update(Config.other_cookie())
    # API: https://vtapi.voicetube.com/v2.1.1/zhTW/pronunciationChallenges/status?platform=Web&userId=1352160&startAt=2018-10-10&endAt=2018-10-20
    # My data: https://vtapi.voicetube.com/v2.1.1/zhTW/pronunciationChallenges/2358/comments?platform=Web&fetchMode=myComments&userId=1352160&page[offset]=0
    api_root = 'https://vtapi.voicetube.com/v2.1.1/zhTW/pronunciationChallenges'
    api_status = 'status?platform={0}&userId={1}&startAt={2}&endAt={3}'.format(
        platform, userId, since.strftime('%Y-%m-%d'), until.strftime('%Y-%m-%d')
    )
    response = same_con.get(
        '{0}/{1}'.format(api_root, api_status),
        headers=headers,
        cookies=cookies
    )
    if hasattr(response, 'status_code') and response.status_code == 200:
        status_res = response.json()
        status_jsons = status_res.get('data')
        for s in status_jsons:
            parameters = '{0}?platform={1}&userId={2}'.format(s.get('id'), platform, userId)
            single_page = same_con.get(
                '{0}/{1}'.format(api_root, parameters),
                headers=headers,
                cookies=cookies
            )
            if hasattr(response, 'status_code') and response.status_code == 200:
                day_format = s.get('date', '').replace('-', '')
                page_res = single_page.json()
                json_file = page_res.get('data', {})
                if json_file.get('audioUrl'):
                    host_name  = json_file.get('host', {}).get('displayName')
                    print('開始下載主持人 {0} 錄音:{1}'.format(host_name, day_format))
                    response = requests.get(json_file.get('audioUrl'))
                    if hasattr(response, 'status_code') and response.status_code == 200:
                        with open('{0}/{1}({2})口說挑戰.mp3'.format(host_voices_dir, day_format, host_name), 'wb') as f:
                            f.write(response.content)
                    article = {}
                    is_empty = False
                    content_keys = ['title', 'content', 'vocabularies', 'translatedContent']
                    for key in content_keys:
                        if not json_file.get(key):
                            is_empty = True
                        else:
                            article.setdefault(key, json_file.get(key))
                    # 產生筆記
                    if not is_empty:
                        print('開始產生筆記:{0}'.format(day_format))
                        with open('{0}/vt{1}.md'.format(output_notes, day_format), 'w', encoding='utf8') as note:
                            note.write('# Topic\n\n')
                            note.write('> {0} <br>\n'.format(article['title']))
                            note.write('> {0} <br>\n'.format(article['content']))
                            note.write('> {0} <br>\n\n'.format(article['translatedContent']))
                            note.write('[![Image]({0})](https://www.youtube.com/embed/{1}?rel=0&showinfo=0&cc_load_policy=0&controls=0&autoplay=0&iv_load_policy=3&playsinline=1&wmode=transparent&start={2}&end={3}&enablejsapi=1&origin=https://tw.voicetube.com&widgetid=1)<br>\n'.format(
                                    json_file.get('imageUrl', ''),
                                    json_file.get('youtubeId', ''),
                                    json_file.get('startAt', 0),
                                    (int(json_file.get('startAt', 0)) + int(json_file.get('duration', 0)))
                                )
                            )
                            note.write('Host: {0} \n<br>'.format(host_name))
                            note.write('Today issue: {0}\n'.format(json_file.get('host', {}).get('comment', '')))
                            note.write('<br>\n')
                            note.write('[Host record]({0})\n'.format(json_file.get('audioUrl', '')))
                            note.write('<br><br>\n')
                            note.write('## learning points\n')
                            word_number = 1
                            for words in article['vocabularies']:
                                note.write('{0}. _\n'.format(word_number))
                                word_number += 1
                                for w in words.get('definitions', []):
                                    note.write('\t* {0} [{1}] {2} {3}\n'.format(
                                        w.get('text', ''),
                                        w.get('kk', ''),
                                        w.get('pos', ''),
                                        w.get('content', '')
                                    ))

                download_myrecord = same_con.get(
                    '{0}/{1}/comments?platform={2}&fetchMode=myComments&userId={3}&page[offset]=0'.format(
                        api_root,
                        s.get('id'),
                        platform,
                        userId),
                    headers=headers,
                    cookies=cookies
                )
                download_json = download_myrecord.json()
                my_record = download_json.get('data', [])
                if my_record:
                    my_record_url = my_record[0].get('audioUrl', '')
                    print('開始下載個人錄音:{0},{1}'.format(day_format, my_record_url))
                    response = requests.get(my_record_url)
                    if hasattr(response, 'status_code') and response.status_code == 200:
                        with open('{0}/{1}口說挑戰.mp3'.format(my_voices_dir, day_format), 'wb') as f:
                            f.write(response.content)
                else:
                    print('My record is empty. ', my_record)