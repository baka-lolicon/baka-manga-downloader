from utils.setting import *
from utils.universal import *
args = parse_args()
if args.m:
    for key, value in IMAGE_SOURCE.items():
        print(f"{key}: {value}")
    USE_IMAGE_SOURCE = IMAGE_SOURCE[input("选择漫画源(输入序号)：")]
if USE_IMAGE_SOURCE == 'manhuagui':
    from manhuagui.manhuagui import *
    print('manhuagui')
elif USE_IMAGE_SOURCE == 'dumanwu':
    from dumanwu.dumanwu import *
    print('dumanwu')
print('='*50)