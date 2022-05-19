# import datetime
# import requests
# from typing import List
# import json
# import random
import pymysql
# import base64
# from facebook_crawl_api.function import KeywordSearch
# from facebook_crawl_api.model import SearchResult
#
#
# def get_cookies():
#     sql = 'select cookies from facebook_cookies where state = 1'
#     cursor.execute(sql)
#     res = cursor.fetchall()
#     return random.choice(res)[0]
#
#
# def save_data(data: SearchResult):
#     img_list = data.media
#     image = list()
#     for img in img_list:
#         if 'video' in img:
#             continue
#         headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; PCRT00 Build/N2G48H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36"}
#         response = requests.get(img, headers=headers, proxies=proxies).content
#         encode_img = base64.b64encode(response)
#         image.append(encode_img.decode())
#         print(encode_img.decode())
#     sql = 'insert into facebook_article (story_fbid, publish_time, content, create_time, profile_id, image, key_word) ' \
#           'values (%s, %s, %s, %s, %s, %s, %s)'
#     cursor.execute(sql, (
#         data.story_fbid,
#         data.article_create_time,
#         data.content,
#         datetime.datetime.now(),
#         data.profile_id,
#         json.dumps(image, ensure_ascii=False),
#         'mustang'))
#     db.commit()
#
# def start():
#     cookies = get_cookies()
#     cookies = json.loads(cookies)
#     search = KeywordSearch(proxies=proxies, cookies=cookies)
#     result = search.search('mustang')
#     data_list: List[SearchResult] = result.get('data')
#     for data in data_list:
#         save_data(data)
#     fb_dtsg = result.get('fb_dtsg')
#     for i in range(5):
#         next_url = result.get('next_url')
#         print(next_url)
#         result = search.search('mustang', next_url=next_url, fb_dtsg=fb_dtsg)
#         data_list = result.get('data')
#         for data in data_list:
#             save_data(data)
#


if __name__ == '__main__':
    db = pymysql.connect(
        host='129.146.45.58',
        user='root',
        password='001224',
        port=3306,
        database='facebook_info'
    )
    cursor = db.cursor()
#     proxies = {
#         'http': 'http://127.0.0.1:7892',
#         'https': 'http://127.0.0.1:7892',
#     }
#     start()
    sql = 'select username, password from user_info where username = %s'
    cursor.execute(sql, ('sheridan77',))
    res = cursor.fetchone()
    print(res)

#
#
