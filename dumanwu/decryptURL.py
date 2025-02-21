import subprocess
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
import execjs
import re
import time
import requests
from lxml import html
from utils.setting import *
from utils.universal import *

def decode_data(p, a, c, k, e, read_data):
    with open("decodeJS/dumanwu.js", "r", encoding='utf-8') as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    k = ctx.call('decode_split',k)
    a = int(a)
    c = int(c)
    e = int(e)
    d = {}
    encode_cmd = ctx.call("get_encode",p, a, c, k, e, d)
    pattern = r'.*?"(.*)"'
    encode_data = re.search(pattern,encode_cmd).group(1)
    result = ctx.call('decode_manga',  read_data, encode_data)
    return result

def get_decode_json(source_data,read_data):
    pattern = r"return p}\((.*)\)\)"
    match = re.search(pattern, source_data)
    encode_data = match.group(1)
    p_p = r"('.*?')"
    match_p = re.findall(p_p, encode_data)[0]
    p_k = r"'(.*?)'"
    match_k = re.findall(p_k, encode_data)[1]
    p_a = r"'.*?',(\d+),\d+,'.*?'.*?,.*?"
    match_a = re.findall(p_a, encode_data)[0]
    p_c = r"'.*?',\d+,(\d+),'.*?'"
    match_c = re.findall(p_c, encode_data)[0]
    p_e = r"'.*?',\d+,\d+,'.*?'.*?,(.*?),.*"
    match_e = re.findall(p_e, encode_data)[0]
    decode_json = decode_data(match_p,match_a,match_c,match_k,match_e,read_data)
    return decode_json

def get_images_info(chapter_url):
    for attempt in range(RETRIES):
        try:
            response = requests.get(chapter_url, headers=HEADERS, cookies=COOKIES, proxies=proxies)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print(f"章节链接获取失败: {e}")
            if attempt < RETRIES - 1:
                print(f"正在重试... {attempt + 1}/{RETRIES}")
                time.sleep(DELAY)
            else:
                print("重试次数已用完，获取链接失败。")
    tree = html.fromstring(response.content)
    source = tree.xpath('//script[not(@src)]/text()')[0]
    read = int(tree.xpath('//div[@class="readerContainer"]/@data-id')[0])
    manga_name = clean_path(tree.xpath('//meta[@itemprop="comicname"]/@content')[0])
    chapter_name = clean_path(tree.xpath('//meta[@itemprop="chaptername"]/@content')[0])
    img_urls = get_decode_json(source,read)
    return img_urls, manga_name, chapter_name

def search_manga(query):
    search_url = f"https://www.dumanwu.com/s"
    data = {'k':query}
    response = requests.post(search_url, data=data, headers=HEADERS, proxies=proxies)
    tree = html.fromstring(response.content)
    search_data = tree.xpath('//p[@class="title"]/a')
    titles, hrefs = [], []
    for item in search_data:
        title = item.get('title')
        href = f"https://www.dumanwu.com{item.get('href')}"
        if title:
            titles.append(title)
        if href:
            hrefs.append(href)
    for i, name in enumerate(titles):
        print(f"{i} : {name}")
    return hrefs

def get_chapter_info(menu_url):
    response = requests.get(menu_url, headers=HEADERS, proxies=proxies)
    tree = html.fromstring(response.content)
    a_tags = tree.xpath('//ul/a')
    titles, hrefs = [], []
    for a in a_tags:
        titles.append(a.xpath('./li/text()')[0])
        hrefs.append(f"https://www.dumanwu.com{a.get('href')}")
    get_chapter_url = 'https://www.dumanwu.com/morechapter'
    manga_id = menu_url.rstrip('/').split('/')[-1]
    data = {'id':manga_id}
    response = requests.post(get_chapter_url, data=data, headers=HEADERS, proxies=proxies)
    json_tags = response.json()['data']
    for json_tag in json_tags:
        titles.append(json_tag['chaptername'])
        hrefs.append(f"https://www.dumanwu.com/{manga_id}/{json_tag['chapterid']}.html")
    for i, name in enumerate(titles):
        print(f"{i} : {name};")

    return titles, hrefs