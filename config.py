# -*- coding: utf-8 -*-
"""
閰嶇疆鏂囦欢锛屽瓨鍌ㄨ矾寰勫拰鍩烘湰璁剧疆
"""

import os

# 鏂囦欢璺緞閰嶇疆
DATA_PATH = r'\\xskynas\userdata\quzhupeng\Desktop\my_python_project\浠锋牸琛╘璋冧环琛?xlsx'
INVENTORY_PATH = r'\\xskynas\userdata\quzhupeng\Desktop\my_python_project\浠锋牸琛╘鏀跺彂瀛樻眹鎬昏〃鏌ヨ.xlsx'
SALES_PATH = r'\\xskynas\userdata\quzhupeng\Desktop\my_python_project\浠锋牸琛╘閿€鍞彂绁ㄦ墽琛屾煡璇?xlsx'
PRODUCTION_PATH = r'\\xskynas\userdata\quzhupeng\Desktop\my_python_project\浠锋牸琛╘浜ф垚鍝佸叆搴撳垪琛?xlsx'
INDUSTRY_TREND_PATH = r'\\xskynas\userdata\quzhupeng\Desktop\my_python_project\浠锋牸琛╘灏忔槑鍐滅墽.xlsx'
OUTPUT_DIR = r'杈撳嚭'  # 浣跨敤鐩稿璺緞锛屾寚鍚戝綋鍓嶇洰褰曚笅鐨勮緭鍑烘枃浠跺す

# 娣诲姞缁煎悎鍞环鏁版嵁鐩綍鍜屾枃浠舵ā寮?
COMPREHENSIVE_PRICE_DIR = r"\\xskynas\userdata\quzhupeng\Desktop\my_python_project\浠锋牸琛?
COMPREHENSIVE_PRICE_PATTERN = r"缁煎悎鍞环(\d+\.\d+)\.xlsx"  # 鐢ㄤ簬鍖归厤鏂囦欢鍚嶅苟鎻愬彇鏃ユ湡
# 淇濈暀鏃ч厤缃敤浜庡吋瀹规€э紝浣嗕笉鍐嶄娇鐢?
COMPREHENSIVE_PRICE_PATH = r"\\xskynas\userdata\quzhupeng\Desktop\my_python_project\浠锋牸琛╘缁煎悎鍞环.xlsx"

# 娣诲姞鍗撳垱璧勮浠锋牸鏂囦欢璺緞
CHICKEN_PRICE_PATH = r"\\xskynas\userdata\quzhupeng\Desktop\my_python_project\浠锋牸琛╘楦¤嫍鍘嗗彶浠锋牸.xlsx"
RAW_CHICKEN_PRICE_PATH = r"\\xskynas\userdata\quzhupeng\Desktop\my_python_project\浠锋牸琛╘姣涢浮鍘嗗彶浠锋牸.xlsx"
BREAST_PRICE_PATH = r"\\xskynas\userdata\quzhupeng\Desktop\my_python_project\浠锋牸琛╘鏉垮喕澶ц兏鍘嗗彶浠锋牸.xlsx"
LEG_PRICE_PATH = r"\\xskynas\userdata\quzhupeng\Desktop\my_python_project\浠锋牸琛╘鐞电惗鑵垮巻鍙蹭环鏍?xlsx"

# 纭繚杈撳嚭鐩綍瀛樺湪
os.makedirs(OUTPUT_DIR, exist_ok=True)



