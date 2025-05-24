# -*- coding: utf-8 -*-
"""
宸ュ叿鍑芥暟妯″潡锛屾彁渚涘悇绉嶈緟鍔╁嚱鏁?
"""

import re
import os
import zipfile
from datetime import datetime


def extract_date_info(sheet_name):
    """
    浠巗heet鍚嶇О涓彁鍙栨棩鏈熷拰璋冧环娆℃暟淇℃伅
    
    鍙傛暟:
        sheet_name: sheet鍚嶇О锛屽'3.7(3)'
        
    杩斿洖:
        (month, day, change_count): 鏈堜唤銆佹棩鏈熷拰璋冧环娆℃暟鐨勫厓缁?
    """
    pattern = r'(\d+)\.(\d+)(?:\((\d+)\))?'
    match = re.match(pattern, sheet_name)
    
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        change_count = int(match.group(3)) if match.group(3) else 1
        return (month, day, change_count)
    return None


def create_zip_archive(output_dir, files_to_exclude=None):
    """
    鍒涘缓ZIP鍘嬬缉鍖?
    
    鍙傛暟:
        output_dir: 杈撳嚭鐩綍
        files_to_exclude: 瑕佹帓闄ょ殑鏂囦欢鍒楄〃
    """
    today = datetime.now().strftime("%Y%m%d")
    zip_path = os.path.join(output_dir, f"{today}_浠锋牸娉㈠姩鍒嗘瀽.zip")
    
    if files_to_exclude is None:
        files_to_exclude = [f"{today}_浠锋牸娉㈠姩鍒嗘瀽.zip"]
    else:
        files_to_exclude.append(f"{today}_浠锋牸娉㈠姩鍒嗘瀽.zip")
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                # 璺宠繃鎺掗櫎鐨勬枃浠?
                if file in files_to_exclude:
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)
    
    print(f"ZIP鍘嬬缉鍖呭凡鍒涘缓: {zip_path}")
    return zip_path 