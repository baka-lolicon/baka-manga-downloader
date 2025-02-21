from utils.choose import *
if __name__ == "__main__":
    if args.s:
        search_content = search_manga(args.s)
        choice = int(input("请选择漫画（输入编号）: "))
        titles, hrefs = get_chapter_info(search_content[choice])
        if args.a:
            print('准备下载所有章节...')
            print('='*50)
            for i, name in enumerate(titles):
                print(f'准备下载: {name}')
                download_chapter_image(hrefs[i])
                print('-'*50)
        elif args.c:
            choice_start = input(f"请选择起始章节（输入编号，从0开始，默认为 0）: ")
            choice_end = input(f"请选择结束章节（输入编号，包含此章节，默认为 {len(titles)-1}）: ")
            choice_start = int(choice_start.strip()) if choice_start.strip() else 0
            choice_end = int(choice_end.strip()) if choice_end.strip() else len(titles) - 1
            print('='*50)
            if 0 <= choice_start <= choice_end <= (len(titles) - 1):
                for i in range(choice_start,choice_end + 1):
                    print(f'准备下载: {titles[i]}')
                    download_chapter_image(hrefs[i])
                    print('-'*50)
            else:
                print('输入异常')
                
        else:
            choice = int(input("请选择下载内容（输入编号）: "))
            print('='*50)
            download_chapter_image(hrefs[choice])
            print('-'*50)
    else:
        print("使用 -h 查看如何使用")