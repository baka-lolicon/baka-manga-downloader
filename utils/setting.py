import json
def load_config(file_path='config.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
config = load_config()
HEADERS = config['HEADERS']
COOKIES = config['COOKIES']
PROXY_IP = config['PROXY_IP']
PROXY_PORT = config['PROXY_PORT']
DOWNLOAD_MAX_WORKERS = config['DOWNLOAD_MAX_WORKERS']
RETRIES = config['RETRIES']
DELAY = config['DELAY']
DOWNLOAD_DIR = config['DOWNLOAD_DIR']
USE_PROXY = config['USE_PROXY']
IMAGE_SOURCE = config['IMAGE_SOURCE']
DEFAULT_IMAGE_SOURCE = config['DEFAULT_IMAGE_SOURCE']
USE_IMAGE_SOURCE = IMAGE_SOURCE[DEFAULT_IMAGE_SOURCE]
if USE_PROXY:
    proxies = {
        'http': f'http://{PROXY_IP}:{PROXY_PORT}',
        'https': f'http://{PROXY_IP}:{PROXY_PORT}'
    }
else:
    proxies = None