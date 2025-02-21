from dumanwu.decryptURL import *
def download_chapter_image(chapter_url):
    img_urls, manga_name, chapter_name = get_images_info(chapter_url)
    download_activate(img_urls, manga_name, chapter_name)