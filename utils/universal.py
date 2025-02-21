import re
import os
import time
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from utils.setting import *

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", action="store_true", help="临时选择漫画下载源")
    group0 = parser.add_mutually_exclusive_group()
    group0.add_argument('-s', type=str, help='搜索，后跟搜索内容')
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('-a', action='store_true', help='下载选择漫画的所有章节')
    group1.add_argument('-c', action='store_true', help='自定义选择下载漫画的章节范围')
    return parser.parse_args()

def download_activate(img_urls, manga_name, chapter_name):

    save_path = f"{DOWNLOAD_DIR}/{manga_name}/{chapter_name}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f'已创建目录：{save_path}')
    with ThreadPoolExecutor(max_workers=DOWNLOAD_MAX_WORKERS) as executor:
        futures = []
        for index, url in enumerate(img_urls):
            future = executor.submit(save_image, url, save_path, index)
            futures.append(future)

        for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading images"):
            future.result()
    
def save_image(image_url, chapter_title, page_number):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.manhuagui.com/"
    }
    file_path = f"{chapter_title}/{page_number}.jpg"
    if os.path.exists(file_path):
        print(f"文件 {file_path} 已存在，跳过下载。")
        return
    for attempt in range(RETRIES):
        try:
            response = requests.get(image_url, headers=headers, proxies=proxies)
            response.raise_for_status()
            with open(file_path , "wb") as file:
                file.write(response.content)
            break
        except requests.exceptions.RequestException as e:
            print(f"下载失败: {e}")
            if attempt < RETRIES - 1:
                print(f"正在重试... {attempt + 1}/{RETRIES}")
                time.sleep(DELAY)
            else:
                print("重试次数已用完，下载失败。")
                failure_file_path = f"./{chapter_title.split('/')[0]}/failure.txt"
                with open(failure_file_path, "a") as failure_file:
                    failure_file.write(f"{file_path} 下载失败：{e}\n")

def clean_path(path):
    illegal_characters = r'[<>:"/\\|?*]'
    return re.sub(illegal_characters, '_', path)