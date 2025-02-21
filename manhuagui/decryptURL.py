import subprocess
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
import execjs
import re
import json
import time
import requests
from lxml import html
import lzstring
from utils.setting import *
from utils.universal import *


def extract_json_from_string(data):
    pattern = r"SMH\.imgData\((.*?)\)\.preInit\(\);"
    match = re.search(pattern, data)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print("JSON解析失败:", e)
            return None
    else:
        print("未找到匹配的 JSON 部分")
        return None

def decode_data(p, a, c, k, e):
    with open("decodeJS/manhuagui.js", "r") as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    k = ctx.call('decode_splic',k)
    a = int(a)
    c = int(c)
    e = int(e)
    d = {}
    result = ctx.call("decode_manga",p, a, c, k, e, d)
    return extract_json_from_string(result)
    
def get_decode_json(source_data):
    pattern = r"return p;}\((.*)\)\)"
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
    decode_json = decode_data(match_p,match_a,match_c,match_k,match_e)
    return decode_json
    
def get_image_url(img_list,url_path,sl_e,sl_m):
    main_url = 'https://eu.hamreus.com'
    main_url += url_path
    img_urls = []
    for i in img_list:
        img_url = f"{main_url}{i}?e={sl_e}&m={sl_m}"
        img_urls.append(img_url)
    return img_urls

def search_manga(query):
    search_url = f"https://www.manhuagui.com/s/{query}.html"
    response = requests.get(search_url, headers=HEADERS, cookies=COOKIES, proxies=proxies)
    tree = html.fromstring(response.content)
    search_data = tree.xpath('//dt/a')

    titles, hrefs = [], []
    for item in search_data:
        title = item.get('title')
        href = f"https://www.manhuagui.com{item.get('href')}"
        if title:
            titles.append(title)
        if href:
            hrefs.append(href)

    for i, name in enumerate(titles):
        print(f"{i} : {name}")
    return hrefs

def get_chapter_info(menu_url):
    response = requests.get(menu_url, headers=HEADERS, cookies=COOKIES, proxies=proxies)
    tree = html.fromstring(response.content)
    input_element = tree.xpath('//input[@id="__VIEWSTATE"]')

    if input_element:
        value = input_element[0].get("value")
        decoded_html = lzstring.LZString().decompressFromBase64(value)
        tree = html.fromstring(decoded_html)
    
    a_tags = tree.xpath('//a[@class="status0"]')
    page_tags = tree.xpath('//a[@class="status0"]/span/i')

    titles, hrefs, pages = [], [], []
    for a in a_tags:
        titles.append(a.get('title'))
        hrefs.append(f"https://www.manhuagui.com{a.get('href')}")

    for page in page_tags:
        pages.append(page.text)

    for i, name in enumerate(titles):
        print(f"{i} : {name};       本章页数：{pages[i]}")

    return titles, hrefs


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
    source = tree.xpath('//script[not(@src)]/text()')[-1]
    img_list = get_decode_json(source)['files']
    url_path = get_decode_json(source)['path']
    sl_e = get_decode_json(source)['sl']['e']
    sl_m = get_decode_json(source)['sl']['m']
    manga_name = clean_path(get_decode_json(source)['bname'])
    chapter_name = clean_path(get_decode_json(source)['cname'])
    img_urls = get_image_url(img_list,url_path,sl_e,sl_m)
    return img_urls, manga_name, chapter_name