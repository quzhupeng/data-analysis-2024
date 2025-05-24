# -*- coding: utf-8 -*-
"""
鏁版嵁鍔犺浇妯″潡锛屽鐞嗗悇绉嶆暟鎹簮鐨勫姞杞藉拰棰勫鐞?"""

import os
import re
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import glob

import config


def extract_date_info(sheet_name):
    """
    浠巗heet鍚嶇О涓彁鍙栨棩鏈熷拰璋冧环娆℃暟淇℃伅
  
    鍙傛暟:
        sheet_name: sheet鍚嶇О锛屽'浠锋牸琛?鏈?鍙凤紙2锛?鎴?浠锋牸琛?鏈?鍙?
      
    杩斿洖:
        (month, day, change_count): 鏈堜唤銆佹棩鏈熷拰璋冧环娆℃暟鐨勫厓缁勶紝鎴栬€匩one
    """
    # 鏂扮殑姝ｅ垯琛ㄨ揪寮忔ā寮忥紝鍖归厤"浠锋牸琛╔鏈圷鍙?鍜?浠锋牸琛╔鏈圷鍙凤紙Z锛?鏍煎紡
    # 浣跨敤涓枃鎷彿
    pattern = r'浠锋牸琛?\d+)鏈?\d+)鍙??:锛?\d+)锛??'
    match = re.match(pattern, sheet_name)
  
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        # 濡傛灉group(3)瀛樺湪锛岃鏄庢湁鎷彿鍐呯殑鏁板瓧锛屽惁鍒欓粯璁や负1
        change_count = int(match.group(3)) if match.group(3) else 1
        return (month, day, change_count)
  
    # 淇濈暀鍘熸潵鐨勬ā寮忓尮閰嶄綔涓哄閫夛紝浠ラ槻鏈変簺sheet杩樹娇鐢ㄦ棫鏍煎紡 (渚嬪 4.2(2))
    old_pattern = r'(\d+)\.(\d+)(?:\((\d+)\))?' # Ensure correct escaping for literal dots and parens
    match = re.match(old_pattern, sheet_name)
  
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        change_count = int(match.group(3)) if match.group(3) else 1
        return (month, day, change_count)

    print(f"鏃犳硶浠巗heet鍚嶇О '{sheet_name}' 涓彁鍙栨棩鏈熶俊鎭紝璺宠繃澶勭悊") # Add print statement for debugging
    return None


class DataLoader:
    """鏁版嵁鍔犺浇鍜岄澶勭悊绫?""
    
    def __init__(self):
        """鍒濆鍖栨暟鎹姞杞藉櫒"""
        self.all_data = pd.DataFrame()
        self.inventory_data = None
        self.sales_data = None
        self.daily_production_data = None
        self.industry_trend_data = None
        self.missing_dates = []
        
    def preprocess_sheet(self, df, sheet_name):
        """
        棰勫鐞嗗崟涓猻heet涓殑鏁版嵁锛屽皢涓変釜骞舵帓鐨勬ā鏉跨旱鍚戝悎骞?        
        鍙傛暟:
            df: 鍘熷DataFrame
            sheet_name: sheet鍚嶇О
            
        杩斿洖:
            processed_df: 澶勭悊鍚庣殑DataFrame
        """
        # 鎻愬彇鏃ユ湡淇℃伅
        date_info = extract_date_info(sheet_name)
        if not date_info:
            print(f"鏃犳硶浠巗heet鍚嶇О '{sheet_name}' 涓彁鍙栨棩鏈熶俊鎭紝璺宠繃澶勭悊")
            return None
        
        month, day, change_count = date_info
        date_str = f"2025-{month:02d}-{day:02d}"  # 鍋囪骞翠唤涓?025
        
        # 妫€鏌ユ暟鎹槸鍚︿负绌?        if df.empty:
            print(f"Sheet '{sheet_name}' 涓病鏈夋暟鎹紝璺宠繃澶勭悊")
            return None
        
        # 瀹氫箟涓変釜妯℃澘鐨勫垪鑼冨洿
        templates = [
            (0, 9),   # 绗竴涓ā鏉? 鍒?-8
            (9, 18),  # 绗簩涓ā鏉? 鍒?-17
            (18, 27)  # 绗笁涓ā鏉? 鍒?8-26
        ]
        
        # 鍒涘缓涓€涓┖鐨凞ataFrame鏉ュ瓨鍌ㄥ悎骞跺悗鐨勬暟鎹?        merged_data = []
        
        # 澶勭悊姣忎釜妯℃澘
        for start_col, end_col in templates:
            if start_col >= df.shape[1]:
                continue  # 濡傛灉鍒楁暟涓嶅锛岃烦杩囨妯℃澘
            
            # 鎻愬彇褰撳墠妯℃澘鐨勬暟鎹?            template_df = df.iloc[:, start_col:end_col].copy()
            
            # 閲嶅懡鍚嶅垪
            if template_df.shape[1] >= 9:  # 纭繚鍒楁暟瓒冲
                template_df.columns = [
                    '鍒嗙被', '鍝佸悕', '瑙勬牸',
                    '鍔犲伐涓€鍘?璋冨箙', '鍔犲伐涓€鍘?鍓嶄环鏍?, '鍔犲伐涓€鍘?浠锋牸',
                    '鍔犲伐浜屽巶-璋冨箙', '鍔犲伐浜屽巶-鍓嶄环鏍?, '鍔犲伐浜屽巶-浠锋牸'
                ]
                
                # 鍒犻櫎绌鸿
                template_df = template_df.dropna(subset=['鍝佸悕'], how='all')
                
                # 蹇界暐鎵€鏈夊寘鍚?鍧囦环"鎴?鍝佸悕"鐨勮
                template_df = template_df[~template_df['鍝佸悕'].astype(str).str.contains('鍧囦环|鍝佸悕')]
                
                # 鍙繚鐣欏姞宸ヤ簩鍘傜殑鏁版嵁
                template_df = template_df[['鍒嗙被', '鍝佸悕', '瑙勬牸', '鍔犲伐浜屽巶-璋冨箙', '鍔犲伐浜屽巶-鍓嶄环鏍?, '鍔犲伐浜屽巶-浠锋牸']]
                template_df.columns = ['鍒嗙被', '鍝佸悕', '瑙勬牸', '璋冨箙', '鍓嶄环鏍?, '浠锋牸']
                
                # 娣诲姞鏃ユ湡鍜岃皟浠锋鏁颁俊鎭?                template_df['鏃ユ湡'] = date_str
                template_df['璋冧环娆℃暟'] = change_count
                
                merged_data.append(template_df)
        
        # 鍚堝苟鎵€鏈夋ā鏉跨殑鏁版嵁
        if merged_data:
            processed_df = pd.concat(merged_data, ignore_index=True)
            
            # 鍒犻櫎閲嶅琛?            processed_df = processed_df.drop_duplicates(subset=['鍝佸悕', '瑙勬牸'], keep='first')
            
            # 纭繚鏁板€煎垪涓烘暟鍊肩被鍨?            for col in ['璋冨箙', '鍓嶄环鏍?, '浠锋牸']:
                processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')
            
            return processed_df
        
        return None
    
    def load_and_process_price_data(self, data_path=None):
        """鍔犺浇骞跺鐞嗕环鏍兼暟鎹?""
        print("寮€濮嬪姞杞藉拰澶勭悊浠锋牸鏁版嵁...")
        
        if data_path is None:
            data_path = config.DATA_PATH
        
        # 妫€鏌ヨ矾寰勬槸鏂囦欢杩樻槸鐩綍
        if os.path.isfile(data_path):
            # 濡傛灉鏄枃浠讹紝鐩存帴澶勭悊杩欎釜鏂囦欢
            excel_files = [os.path.basename(data_path)]
            file_dir = os.path.dirname(data_path)
        elif os.path.isdir(data_path):
            # 濡傛灉鏄洰褰曪紝鑾峰彇鐩綍涓殑鎵€鏈塃xcel鏂囦欢
            excel_files = [f for f in os.listdir(data_path) if f.endswith('.xlsx') or f.endswith('.xls')]
            file_dir = data_path
        else:
            print(f"璺緞 {data_path} 鏃笉鏄枃浠朵篃涓嶆槸鐩綍")
            return
        
        if not excel_files:
            print(f"鍦ㄨ矾寰?{data_path} 涓病鏈夋壘鍒癊xcel鏂囦欢")
            return
        
        all_sheets_data = []
        date_records = set()  # 鐢ㄤ簬璁板綍宸插鐞嗙殑鏃ユ湡
        
        for file in excel_files:
            if os.path.isfile(data_path):
                file_path = data_path
            else:
                file_path = os.path.join(file_dir, file)
            
            print(f"澶勭悊鏂囦欢: {file}")
            
            try:
                # 璇诲彇Excel鏂囦欢涓殑鎵€鏈塻heet
                excel = pd.ExcelFile(file_path)
                
                # 鎸夌収鏃ユ湡椤哄簭鎺掑簭sheet
                def sheet_sort_key(sheet_name):
                    date_info = extract_date_info(sheet_name)
                    if date_info:
                        month, day, count = date_info
                        return (month, day, count)
                    return (0, 0, 0)
                
                sorted_sheets = sorted(excel.sheet_names, key=sheet_sort_key)
                
                for sheet_name in sorted_sheets:
                    print(f"  澶勭悊sheet: {sheet_name}")
                    
                    # 璇诲彇sheet鏁版嵁
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    
                    # 棰勫鐞唖heet鏁版嵁
                    processed_df = self.preprocess_sheet(df, sheet_name)
                    
                    if processed_df is not None and not processed_df.empty:
                        all_sheets_data.append(processed_df)
                        
                        # 璁板綍鏃ユ湡
                        date_info = extract_date_info(sheet_name)
                        if date_info:
                            month, day, _ = date_info
                            date_records.add((month, day))
            
            except Exception as e:
                print(f"澶勭悊鏂囦欢 {file} 鏃跺嚭閿? {str(e)}")
        
        # 鍚堝苟鎵€鏈塻heet鐨勬暟鎹?        if all_sheets_data:
            self.all_data = pd.concat(all_sheets_data, ignore_index=True)
            print(f"鎴愬姛鍔犺浇 {len(self.all_data)} 鏉℃暟鎹褰?)
            
            # 妫€鏌ユ棩鏈熻繛缁€?            self.check_date_continuity(date_records)
        else:
            print("娌℃湁鎴愬姛鍔犺浇浠讳綍鏁版嵁")
        
        return self.all_data
    
    def check_date_continuity(self, date_records):
        """
        妫€鏌ユ棩鏈熺殑杩炵画鎬?        
        鍙傛暟:
            date_records: 鍖呭惈(鏈?鏃?鍏冪粍鐨勯泦鍚?        """
        # 灏?鏈?鏃?杞崲涓烘棩鏈熷璞?        current_year = datetime.now().year
        dates = [datetime(current_year, month, day) for month, day in date_records]
        dates.sort()
        
        # 妫€鏌ユ棩鏈熻繛缁€?        for i in range(len(dates) - 1):
            current_date = dates[i]
            next_date = dates[i + 1]
            delta = (next_date - current_date).days
            
            if delta > 1:
                # 鎵惧嚭缂哄け鐨勬棩鏈?                missing_date = current_date + timedelta(days=1)
                while missing_date < next_date:
                    self.missing_dates.append(missing_date.strftime("%Y-%m-%d"))
                    missing_date += timedelta(days=1)
        
        if self.missing_dates:
            print(f"鍙戠幇缂哄け鐨勬棩鏈? {', '.join(self.missing_dates)}")
    
    def load_inventory_data(self, inventory_path=None):
        """鍔犺浇搴撳瓨鏁版嵁锛堜笉鍖呭惈椴滃搧鍜屽壇浜у搧锛?""
        print("寮€濮嬪姞杞藉簱瀛樻暟鎹?..")
        
        if inventory_path is None:
            inventory_path = config.INVENTORY_PATH
        
        try:
            # 璇诲彇搴撳瓨琛?            inventory_df = pd.read_excel(inventory_path)
            
            # 鎵撳嵃鍒楀悕锛屽府鍔╄皟璇?            print("搴撳瓨琛ㄧ殑鍒楀悕:")
            for col in inventory_df.columns:
                print(f"  - '{col}' (绫诲瀷: {type(col).__name__})")
            
            # 鍩烘湰鏁版嵁娓呮礂
            if not inventory_df.empty:
                # 鍒犻櫎鍏ㄧ┖琛屽拰鍝佸悕涓虹┖鐨勮
                inventory_df = inventory_df.dropna(how='all')
                inventory_df = inventory_df[inventory_df['鐗╂枡鍚嶇О'].notna() & (inventory_df['鐗╂枡鍚嶇О'] != '')]
                
                # 杩囨护鎺夊鎴蜂负"鍓骇鍝?銆?椴滃搧"鎴栫┖鐧界殑璁板綍
                if '瀹㈡埛' in inventory_df.columns:
                    original_count_customer_filter = len(inventory_df)
                    # 纭繚瀹㈡埛鍒楁槸瀛楃涓茬被鍨嬪苟鍘婚櫎棣栧熬绌烘牸
                    inventory_df['瀹㈡埛'] = inventory_df['瀹㈡埛'].astype(str).str.strip()
                    excluded_customers_values = ['鍓骇鍝?, '椴滃搧', ''] # 娣诲姞绌哄瓧绗︿覆鍒版帓闄ゅ垪琛?                    mask = ~inventory_df['瀹㈡埛'].isin(excluded_customers_values)
                    inventory_df = inventory_df[mask]
                    print(f"鎺掗櫎瀹㈡埛涓?鍓骇鍝?銆?椴滃搧'鎴栫┖鐧界殑鏁版嵁鍚庯紝浠?{original_count_customer_filter} 鏉¤褰曚腑鍓╀綑 {len(inventory_df)} 鏉¤褰?)
                
                # 鏂板锛氭牴鎹?鐗╂枡鍒嗙被鍚嶇О"鍒楄繘琛岀瓫閫?                material_category_col = '鐗╂枡鍒嗙被鍚嶇О' # 鍋囪Excel涓殑
                if material_category_col in inventory_df.columns:
                    excluded_categories = ['鍓骇鍝?, '鐢熼矞鍝佸叾浠?] # 鏇存柊鎺掗櫎鍒楄〃
                    # 棣栧厛澶勭悊绌哄瓧绗︿覆锛屽皢鍏舵浛鎹负 NaN锛屼互渚垮悗缁?.isin() 鍙互姝ｇ‘澶勭悊
                    inventory_df[material_category_col] = inventory_df[material_category_col].replace(r'^\s*$', np.nan, regex=True)
                    
                    # 鏋勫缓鎺掗櫎 NaN 鍜岀壒瀹氬垎绫荤殑鎺╃爜
                    mask = ~(
                        inventory_df[material_category_col].isin(excluded_categories) | \
                        inventory_df[material_category_col].isna()
                    )
                    original_count = len(inventory_df)
                    inventory_df = inventory_df[mask]
                    print(f"鏍规嵁'鐗╂枡鍒嗙被鍚嶇О'鎺掗櫎鐗瑰畾鍒嗙被锛堢┖鐧姐€佸壇浜у搧銆佺敓椴滃搧鍏朵粬锛夊悗锛屼粠 {original_count} 鏉¤褰曚腑鍓╀綑 {len(inventory_df)} 鏉¤褰?) # 鏇存柊鎵撳嵃淇℃伅
                else:
                    print(f"璀﹀憡: 搴撳瓨鏁版嵁涓湭鎵惧埌鍒?'{material_category_col}'锛屾棤娉曞簲鐢ㄧ墿鏂欏垎绫诲悕绉扮瓫閫夈€?)
                
                # 鏂板锛氭帓闄ょ墿鏂欏悕绉板惈"椴?瀛楃殑璁板綍
                original_count = len(inventory_df)
                inventory_df = inventory_df[~inventory_df['鐗╂枡鍚嶇О'].astype(str).str.contains('椴?, case=False, na=False)]
                print(f"鎺掗櫎鐗╂枡鍚嶇О鍚?椴?瀛楃殑璁板綍鍚庯紝浠?{original_count} 鏉¤褰曚腑鍓╀綑 {len(inventory_df)} 鏉¤褰?)
                
                # 瀹氫箟鍒楀悕鏄犲皠
                column_mapping = {
                    '鐗╂枡鍚嶇О': '鍝佸悕',
                    '鍏ュ簱': '浜ч噺',
                    '鍑哄簱': '閿€閲?,
                    '缁撳瓨': '搴撳瓨閲?
                }
                
                # 閲嶅懡鍚嶅垪
                inventory_df = inventory_df.rename(columns=column_mapping)
                
                # 鏁版嵁绫诲瀷杞崲
                numeric_columns = ['浜ч噺', '閿€閲?, '搴撳瓨閲?]
                for col in numeric_columns:
                    if col in inventory_df.columns:
                        inventory_df[col] = pd.to_numeric(inventory_df[col], errors='coerce')
                
                # 鎺掑簭
                inventory_df = inventory_df.sort_values(by=['鍝佸悕'], ascending=True)
                
                self.inventory_data = inventory_df
                print(f"鎴愬姛鍔犺浇 {len(inventory_df)} 鏉″簱瀛樿褰?)
                return inventory_df
            else:
                print("搴撳瓨琛ㄤ负绌?)
                return None
        
        except Exception as e:
            print(f"鍔犺浇搴撳瓨鏁版嵁鏃跺嚭閿? {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def load_sales_data(self, sales_path=None):
        """鍔犺浇閿€鍞暟鎹紙鐢ㄤ簬缁樺埗閿€鍞秼鍔垮浘锛屾帓闄ゅ鎴峰悕绉颁负绌恒€佸壇浜у搧銆侀矞鍝佺殑璁板綍锛?""
        print("寮€濮嬪姞杞介攢鍞暟鎹?(缁熶竴娓呮礂瑙勫垯)...")
        
        if sales_path is None:
            sales_path = config.SALES_PATH
        
        try:
            # 璇诲彇閿€鍞暟鎹?            sales_df = pd.read_excel(sales_path)
            
            # 鎵撳嵃鍒楀悕锛屽府鍔╄皟璇?            print("鍘熷閿€鍞暟鎹殑鍒楀悕:")
            for col in sales_df.columns:
                print(f"  - '{col}' (绫诲瀷: {type(col).__name__})")
            
            if sales_df.empty:
                print("閿€鍞暟鎹枃浠朵负绌?)
                return None

            # 鍒犻櫎鍏ㄧ┖琛?            sales_df = sales_df.dropna(how='all')
            print(f"鍒犻櫎鍏ㄧ┖琛屽悗锛屽墿浣?{len(sales_df)} 鏉¤褰?)

            # 妫€鏌ュ熀鏈棩鏈熷垪鏄惁瀛樺湪
            date_column_name = '鍙戠エ鏃ユ湡'
            if date_column_name not in sales_df.columns:
                print(f"閿欒: 閿€鍞暟鎹己灏戝繀瑕佺殑鏃ユ湡鍒?'{date_column_name}'")
                return None
            sales_df[date_column_name] = pd.to_datetime(sales_df[date_column_name], errors='coerce')
            sales_df = sales_df.dropna(subset=[date_column_name])
            print(f"杞崲 '{date_column_name}' 骞剁Щ闄ゆ棤鏁堟棩鏈熷悗锛屽墿浣?{len(sales_df)} 鏉¤褰?)

            # 娓呮礂鏉′欢 1: 鐗╂枡鍒嗙被鍒楋紝鍘婚櫎"鍓骇鍝?銆?绌虹櫧"鐨勮
            material_category_column = '鐗╂枡鍒嗙被' 
            if material_category_column in sales_df.columns:
                print(f"搴旂敤鐗╂枡鍒嗙被绛涢€夊墠: {len(sales_df)} 鏉¤褰?)
                sales_df[material_category_column] = sales_df[material_category_column].replace(r'^\\s*$', np.nan, regex=True)
                sales_df = sales_df[
                    (~sales_df[material_category_column].astype(str).str.lower().isin(['鍓骇鍝?, 'nan', '']))
                ]
                print(f'绛涢€夋帀"鐗╂枡鍒嗙被"涓?鍓骇鍝?鎴栫┖鐧藉悗锛屽墿浣?{len(sales_df)} 鏉¤褰?)
            else:
                print(f"璀﹀憡: 鏈壘鍒板垪 '{material_category_column}'锛屾棤娉曞簲鐢ㄧ墿鏂欏垎绫荤瓫閫夈€?)

            # 娓呮礂鏉′欢 2: 瀹㈡埛鍚嶇О鍒楋紝鎺掗櫎瀹㈡埛鍚嶇О涓虹┖銆?鍓骇鍝?鎴?椴滃搧"鐨勮褰?            customer_name_column = '瀹㈡埛鍚嶇О' 
            if customer_name_column in sales_df.columns:
                print(f"娓呮礂鍓?瀹㈡埛鍚嶇О'绛涢€夛紝璁板綍鏁? {len(sales_df)}")
                # 纭繚涓哄瓧绗︿覆绫诲瀷骞跺幓闄ら灏剧┖鏍硷紝澶勭悊娼滃湪鐨?NaN 鍊?                sales_df[customer_name_column] = sales_df[customer_name_column].fillna('').astype(str).str.strip()
                
                # 瀹氫箟瑕佹帓闄ょ殑瀹㈡埛鍚嶇О鍒楄〃 (缁熶竴灏忓啓浠ヨ繘琛屼笉鍖哄垎澶у皬鍐欑殑姣旇緝)
                excluded_customer_names_lower = ['', '鍓骇鍝?.lower(), '椴滃搧'.lower()] 
                
                # 搴旂敤鎺掗櫎绛涢€?(灏嗗垪鍐呭杞负灏忓啓杩涜姣旇緝)
                sales_df = sales_df[~sales_df[customer_name_column].str.lower().isin(excluded_customer_names_lower)]
                print(f'鎸夋柊瑙勫垯绛涢€?瀹㈡埛鍚嶇О"锛堟帓闄ょ┖鐧姐€佸壇浜у搧銆侀矞鍝侊級鍚庯紝鍓╀綑 {len(sales_df)} 鏉¤褰?)
            else:
                print(f"璀﹀憡: 鏈壘鍒板垪 '{customer_name_column}'锛屾棤娉曞簲鐢ㄥ鎴峰悕绉扮瓫閫夈€?)

            # 娓呮礂鏉′欢 3: 鐗╂枡鍚嶇О"鍒楋紝鍒犻櫎鍏朵腑鍖呭惈"椴?鐨勮褰?            material_name_column = '鐗╂枡鍚嶇О' 
            if material_name_column in sales_df.columns:
                print(f"搴旂敤鐗╂枡鍚嶇О绛涢€夊墠: {len(sales_df)} 鏉¤褰?)
                sales_df = sales_df[
                    ~sales_df[material_name_column].astype(str).str.contains('椴?, case=False, na=False)
                ]
                print(f'鍒犻櫎"鐗╂枡鍚嶇О"鍖呭惈"椴?鐨勮褰曞悗锛屽墿浣?{len(sales_df)} 鏉¤褰?)    
            else:
                print(f"璀﹀憡: 鏈壘鍒板垪 '{material_name_column}'锛屾棤娉曞簲鐢ㄧ墿鏂欏悕绉扮瓫閫夈€?)

            # 娓呮礂鏉′欢 4: 鏁伴噺鍒楃殑纭畾:鍥哄畾浣跨敤"涓绘暟閲?鍒椾綔涓洪攢閲忔潵婧愩€?            quantity_column_to_use = '涓绘暟閲?
            if quantity_column_to_use not in sales_df.columns:
                print(f"閿欒: 閿€鍞暟鎹己灏戝繀瑕佺殑鏁伴噺鍒?'{quantity_column_to_use}'")
                # Potentially return None or an empty DataFrame if this column is critical
                # For now, we will proceed, but downstream process_sales_data will need to handle its absence
                # if it's not present, or we ensure it must exist.
                # To strictly enforce, uncomment: return None 
            else:
                sales_df[quantity_column_to_use] = pd.to_numeric(sales_df[quantity_column_to_use], errors='coerce')
                # Optional: Filter out rows where '涓绘暟閲? is NaN or non-positive, if business logic requires
                sales_df = sales_df.dropna(subset=[quantity_column_to_use])
                # sales_df = sales_df[sales_df[quantity_column_to_use] > 0] # Uncomment if sales must be positive
                print(f"杞崲 '{quantity_column_to_use}' 涓烘暟鍊煎苟绉婚櫎鏃犳晥鏉＄洰鍚庯紝鍓╀綑 {len(sales_df)} 鏉¤褰?)

            # 鍏朵粬蹇呰鐨勫垪锛屽閲戦锛屼篃搴旇繘琛屾鏌ュ拰绫诲瀷杞崲
            amount_column = '鏈竵鏃犵◣閲戦'
            if amount_column in sales_df.columns:
                sales_df[amount_column] = pd.to_numeric(sales_df[amount_column], errors='coerce')
            else:
                print(f"璀﹀憡: 鏈壘鍒伴噾棰濆垪 '{amount_column}'銆傜浉鍏宠绠楀彲鑳藉彈褰卞搷銆?)
                
            # 瀛樺偍缁撴灉
            self.sales_data = sales_df
            
            print(f"鎴愬姛鍔犺浇骞舵寜缁熶竴瑙勫垯娓呮礂鍚庯紝鍓╀綑 {len(sales_df)} 鏉￠攢鍞暟鎹?)
            return self.sales_data
        
        except Exception as e:
            print(f"鍔犺浇閿€鍞暟鎹椂鍑洪敊: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def load_daily_production_data(self, production_path=None):
        """鍔犺浇姣忔棩浜ч噺鏁版嵁锛岀敤浜庤绠椾骇閿€鐜?""
        print("寮€濮嬪姞杞戒骇閲忔暟鎹?..")
        
        if production_path is None:
            production_path = config.PRODUCTION_PATH  # 鐜板湪鎸囧悜"浜ф垚鍝佸叆搴撳垪琛?xlsx"
        
        try:
            # 璇诲彇浜ч噺鏁版嵁
            production_df = pd.read_excel(production_path, engine='openpyxl')
            
            # 鎵撳嵃鍒楀悕锛屽府鍔╄皟璇?            print("浜ч噺鏁版嵁鐨勫垪鍚?")
            for col in production_df.columns:
                print(f"  - '{col}' (绫诲瀷: {type(col).__name__})")
            
            # 鍩烘湰鏁版嵁娓呮礂
            if not production_df.empty:
                # 鍒犻櫎鍏ㄧ┖琛?                production_df = production_df.dropna(how='all')
                
                # 鍒楀悕鏄犲皠 - 閫傞厤鏂扮殑Excel鏍煎紡
                date_column = '鍏ュ簱鏃ユ湡'
                material_column = '鐗╂枡鍚嶇О'
                quantity_column = '涓绘暟閲?
                
                # 妫€鏌ュ繀瑕佺殑鍒楁槸鍚﹀瓨鍦?                required_columns = [date_column, material_column, quantity_column]
                missing_columns = [col for col in required_columns if col not in production_df.columns]
                
                if missing_columns:
                    print(f"浜ч噺鏁版嵁缂哄皯蹇呰鐨勫垪: {', '.join(missing_columns)}")
                    return {'by_material': {}, 'total': {}}
                
                # 鏁版嵁娓呮礂锛氬幓闄ょ墿鏂欏悕绉颁腑鍚?椴?瀛楃殑琛?                if material_column in production_df.columns:
                    production_df = production_df[~production_df[material_column].astype(str).str.contains('椴?)]
                    print(f"鎺掗櫎鐗╂枡鍚嶇О鍚?椴?瀛楃殑璁板綍鍚庯紝鍓╀綑 {len(production_df)} 鏉¤褰?)
                
                # 鏁版嵁娓呮礂锛氬幓鎺夌墿鏂欏ぇ绫讳腑"鍓骇鍝?鍜岀┖鐧?                material_category_column = None
                for col in ['鐗╂枡澶х被', '鐗╂枡鎵€灞炲垎绫?]:
                    if col in production_df.columns:
                        material_category_column = col
                        break
                        
                if material_category_column:
                    # 鍘婚櫎鐗╂枡澶х被涓虹┖鐧界殑璁板綍
                    production_df = production_df[production_df[material_category_column].notna() & 
                                                 (production_df[material_category_column] != '')]
                    print(f"鎺掗櫎鐗╂枡澶х被涓虹┖鐧界殑璁板綍鍚庯紝鍓╀綑 {len(production_df)} 鏉¤褰?)
                    
                    # 鍘婚櫎鐗╂枡澶х被涓?鍓骇鍝?鐨勮褰?                    production_df = production_df[production_df[material_category_column] != '鍓骇鍝?]
                    print(f"鎺掗櫎鐗╂枡澶х被涓?鍓骇鍝?鐨勮褰曞悗锛屽墿浣?{len(production_df)} 鏉¤褰?)
                
                # 杞崲鏃ユ湡鍒椾负鏃ユ湡绫诲瀷
                production_df[date_column] = pd.to_datetime(production_df[date_column], errors='coerce')
                
                # 鍒犻櫎鏃ユ湡涓虹┖鐨勮
                production_df = production_df.dropna(subset=[date_column])
                
                # 杞崲涓绘暟閲忓垪涓烘暟鍊肩被鍨?                production_df[quantity_column] = pd.to_numeric(production_df[quantity_column], errors='coerce')
                
                # 鍒犻櫎涓绘暟閲忎负NaN鐨勮
                production_df = production_df.dropna(subset=[quantity_column])
                
                # 鎸夋棩鏈熷拰鐗╂枡鍚嶇О鍒嗙粍锛屾眹鎬讳骇閲?                daily_production = production_df.groupby([production_df[date_column].dt.date, material_column])[
                    quantity_column].sum().reset_index()
                
                # 鍒涘缓鎸夋棩鏈熷拰鐗╂枡鍒嗙粍鐨勫瓧鍏?                daily_production_dict = {}
                daily_total_production = {}
                
                for _, row in daily_production.iterrows():
                    date = row[date_column]
                    material = row[material_column]
                    quantity = row[quantity_column]
                    
                    if date not in daily_production_dict:
                        daily_production_dict[date] = {}
                        daily_total_production[date] = 0
                    
                    daily_production_dict[date][material] = quantity
                    daily_total_production[date] += quantity
                
                print(f"鎴愬姛鍔犺浇 {len(production_df)} 鏉′骇閲忔暟鎹紝瑕嗙洊 {len(daily_production_dict)} 涓棩鏈?)
                
                # 杩斿洖涓や釜瀛楀吀锛氭寜鐗╂枡鍒嗙粍鐨勫拰姣忔棩鎬讳骇閲?                return {
                    'by_material': daily_production_dict,
                    'total': daily_total_production
                }
            else:
                print("浜ч噺鏁版嵁涓虹┖")
                return {'by_material': {}, 'total': {}}
        
        except Exception as e:
            print(f"鍔犺浇浜ч噺鏁版嵁鏃跺嚭閿? {str(e)}")
            import traceback
            traceback.print_exc()
            return {'by_material': {}, 'total': {}}
    
    def load_industry_trend_data(self, industry_trend_path=None):
        """鍔犺浇琛屼笟瓒嬪娍鏁版嵁"""
        print("寮€濮嬪姞杞借涓氳秼鍔挎暟鎹?..")
        
        if industry_trend_path is None:
            industry_trend_path = config.INDUSTRY_TREND_PATH
        
        try:
            # 璇诲彇琛屼笟瓒嬪娍鏁版嵁
            industry_trend_df = pd.read_excel(industry_trend_path)
            
            # 鎵撳嵃鍒楀悕锛屽府鍔╄皟璇?            print("琛屼笟瓒嬪娍鏁版嵁鐨勫垪鍚?")
            for col in industry_trend_df.columns:
                print(f"  - '{col}' (绫诲瀷: {type(col).__name__})")
            
            # 鍩烘湰鏁版嵁娓呮礂
            if not industry_trend_df.empty:
                # 鍒犻櫎鍏ㄧ┖琛?                industry_trend_df = industry_trend_df.dropna(how='all')
                
                # 杞崲鏃ユ湡鍒?                date_cols = [col for col in industry_trend_df.columns if '鏃ユ湡' in col]
                for col in date_cols:
                    industry_trend_df[col] = pd.to_datetime(industry_trend_df[col], errors='coerce')
                
                # 瀛樺偍缁撴灉
                self.industry_trend_data = industry_trend_df
                
                print(f"鎴愬姛鍔犺浇 {len(industry_trend_df)} 鏉¤涓氳秼鍔挎暟鎹?)
                return industry_trend_df
            else:
                print("琛屼笟瓒嬪娍鏁版嵁涓虹┖")
                return None
        
        except Exception as e:
            print(f"鍔犺浇琛屼笟瓒嬪娍鏁版嵁鏃跺嚭閿? {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def load_price_comparison_data(self, comparison_path=None):
        """鍔犺浇鏄ラ洩涓庡皬鏄庡啘鐗т环鏍煎姣旀暟鎹?""
        print("寮€濮嬪姞杞戒环鏍煎姣旀暟鎹?..")
        
        if comparison_path is None:
            comparison_path = r'\\xskynas\userdata\quzhupeng\Desktop\my_python_project\浠锋牸琛╘鏄ラ洩涓庡皬鏄庡啘鐗т环鏍煎姣?xlsx'
        
        try:
            # 璇诲彇浠锋牸瀵规瘮琛?            comparison_df = pd.read_excel(comparison_path)
            
            # 鎵撳嵃鍒楀悕锛屽府鍔╄皟璇?            print("浠锋牸瀵规瘮琛ㄧ殑鍒楀悕:")
            for col in comparison_df.columns:
                print(f"  - '{col}' (绫诲瀷: {type(col).__name__})")
            
            # 鍩烘湰鏁版嵁娓呮礂
            if not comparison_df.empty:
                # 鍒犻櫎鍏ㄧ┖琛?                comparison_df = comparison_df.dropna(how='all')
                
                # 妫€鏌ュ繀瑕佺殑鍒楁槸鍚﹀瓨鍦?                required_columns = ['鍝佸悕', '瑙勬牸', '鏄ラ洩浠锋牸', '灏忔槑涓棿浠?, '涓棿浠峰樊']
                missing_columns = [col for col in required_columns if col not in comparison_df.columns]
                
                if missing_columns:
                    print(f"浠锋牸瀵规瘮琛ㄧ己灏戝繀瑕佺殑鍒? {', '.join(missing_columns)}")
                    return None
                
                # 纭繚鏁板€煎垪涓烘暟鍊肩被鍨?                for col in ['鏄ラ洩浠锋牸', '灏忔槑涓棿浠?, '涓棿浠峰樊']:
                    comparison_df[col] = pd.to_numeric(comparison_df[col], errors='coerce')
                
                print(f"鎴愬姛鍔犺浇 {len(comparison_df)} 鏉′环鏍煎姣旀暟鎹?)
                return comparison_df
            else:
                print("浠锋牸瀵规瘮琛ㄤ负绌?)
                return None
        
        except Exception as e:
            print(f"鍔犺浇浠锋牸瀵规瘮鏁版嵁鏃跺嚭閿? {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def load_daily_sales_data(self, path):
        """鍔犺浇閿€鍞暟鎹紙鐢ㄤ簬璁＄畻浜ч攢鐜囷紝鎺掗櫎瀹㈡埛鍚嶇О涓虹┖銆佸壇浜у搧銆侀矞鍝佺殑璁板綍锛?""
        # 濡傛灉 path 涓?None锛屽垯浠?config 鏂囦欢鍔犺浇璺緞
        if path is None:
            path = config.SALES_PATH
            print(f"Path was None, using config.SALES_PATH: {path}")
        
        # 妫€鏌ヨ矾寰勬槸鍚﹀瓨鍦?        if not path or not os.path.exists(path):
            print(f"Error: Sales data file not found at path: {path}")
            return {'by_material': {}, 'total': {}} # 杩斿洖绌虹粨鏋?
        print(f"Loading daily sales data from: {path}")
        try:
            sales_df = pd.read_excel(path, engine='openpyxl')
        except FileNotFoundError:
            print(f"Error: File not found at specified path: {path}")
            return {'by_material': {}, 'total': {}} # 杩斿洖绌虹粨鏋?        except Exception as e:
            print(f"Error reading Excel file at {path}: {e}")
            import traceback
            traceback.print_exc()
            return {'by_material': {}, 'total': {}} # 杩斿洖绌虹粨鏋?
        # 鏁版嵁娓呮礂锛氳浆鎹㈡棩鏈熷垪
        date_column_name = '鍙戠エ鏃ユ湡' # 淇鍒楀悕
        if date_column_name in sales_df.columns:
            sales_df[date_column_name] = pd.to_datetime(sales_df[date_column_name], errors='coerce')
            sales_df = sales_df.dropna(subset=[date_column_name])  # 鍒犻櫎鏃ユ湡涓篘aN鐨勮
            print(f"浣跨敤鍒?'{date_column_name}' 杩涜鏃ユ湡杞崲鍜屽鐞嗐€?)
        else:
            print(f"閿欒锛氬湪閿€鍞暟鎹腑鏈壘鍒伴鏈熺殑鏃ユ湡鍒?'{date_column_name}'銆傚彲鐢ㄥ垪锛歿sales_df.columns.tolist()}")
            return {'by_material': {}, 'total': {}} # 鏆傛椂杩斿洖绌?        
        # 娓呮礂鏉′欢 1: 鐗╂枡鍒嗙被鍒楋紝鍘婚櫎"鍓骇鍝?銆?绌虹櫧"鐨勮
        material_category_column = '鐗╂枡鍒嗙被' # 鍋囪鍒楀悕涓?鐗╂枡鍒嗙被'
        if material_category_column in sales_df.columns:
            print(f"鍘熷璁板綍鏁?(娓呮礂鍓嶇墿鏂欏垎绫荤瓫閫?: {len(sales_df)}")
            # 鏇挎崲绌虹櫧瀛楃涓蹭负绌哄€?(NaN) 浠ヤ究缁熶竴澶勭悊
            sales_df[material_category_column] = sales_df[material_category_column].replace(r'^\\s*$', np.nan, regex=True)
            sales_df = sales_df[
                (~sales_df[material_category_column].astype(str).str.lower().isin(['鍓骇鍝?, 'nan', '']))
            ]
            print(f'绛涢€夋帀"鐗╂枡鍒嗙被"涓?鍓骇鍝?鎴栫┖鐧藉悗锛屽墿浣?{len(sales_df)} 鏉¤褰?)
        else:
            print(f"璀﹀憡: 鏈壘鍒板垪 '{material_category_column}'锛屾棤娉曞簲鐢ㄧ墿鏂欏垎绫荤瓫閫夈€?)

        # 娓呮礂鏉′欢 2: 瀹㈡埛鍚嶇О鍒楋紝鎺掗櫎瀹㈡埛鍚嶇О涓虹┖銆?鍓骇鍝?鎴?椴滃搧"鐨勮褰?        customer_name_column = '瀹㈡埛鍚嶇О' # 鍋囪鍒楀悕涓?瀹㈡埛鍚嶇О'
        if customer_name_column in sales_df.columns:
            print(f"娓呮礂鍓?瀹㈡埛鍚嶇О'绛涢€夛紝璁板綍鏁? {len(sales_df)}")
            # 1. 纭繚涓哄瓧绗︿覆绫诲瀷骞跺幓闄ら灏剧┖鏍硷紝澶勭悊娼滃湪鐨?NaN 鍊?            sales_df[customer_name_column] = sales_df[customer_name_column].fillna('').astype(str).str.strip()
            
            # 2. 瀹氫箟瑕佹帓闄ょ殑瀹㈡埛鍚嶇О鍒楄〃 (缁熶竴灏忓啓浠ヨ繘琛屼笉鍖哄垎澶у皬鍐欑殑姣旇緝)
            excluded_customer_names_lower = ['', '鍓骇鍝?.lower(), '椴滃搧'.lower()] 
            
            # 3. 搴旂敤鎺掗櫎绛涢€?(灏嗗垪鍐呭杞负灏忓啓杩涜姣旇緝)
            sales_df = sales_df[~sales_df[customer_name_column].str.lower().isin(excluded_customer_names_lower)]
            print(f'鎸夋柊瑙勫垯绛涢€?瀹㈡埛鍚嶇О"锛堟帓闄ょ┖鐧姐€佸壇浜у搧銆侀矞鍝侊級鍚庯紝鍓╀綑 {len(sales_df)} 鏉¤褰?)
        else:
            print(f"璀﹀憡: 鍒?'{customer_name_column}' 鏈壘鍒帮紝鏃犳硶搴旂敤瀹㈡埛鍚嶇О绛涢€夈€?)

        # 娓呮礂鏉′欢 3: 鐗╂枡鍚嶇О"鍒楋紝鍒犻櫎鍏朵腑鍖呭惈"椴?鐨勮褰?        material_name_column = '鐗╂枡鍚嶇О' # 鍋囪鍒楀悕涓?鐗╂枡鍚嶇О'
        if material_name_column in sales_df.columns:
            print(f"鍘熷璁板綍鏁?(娓呮礂鍓嶇墿鏂欏悕绉扮瓫閫?: {len(sales_df)}")
            sales_df = sales_df[
                ~sales_df[material_name_column].astype(str).str.contains('椴?, case=False, na=False)
            ]
            print(f'鍒犻櫎"鐗╂枡鍚嶇О"鍖呭惈"椴?鐨勮褰曞悗锛屽墿浣?{len(sales_df)} 鏉¤褰?)   
        else:
            print(f"璀﹀憡: 鏈壘鍒板垪 '{material_name_column}'锛屾棤娉曞簲鐢ㄧ墿鏂欏悕绉扮瓫閫夈€?)
        
        # 娓呮礂鏉′欢 4: 鏁伴噺鍒楃殑纭畾:鍥哄畾浣跨敤"涓绘暟閲?鍒椾綔涓洪攢閲忔潵婧愩€?        quantity_column_name = '涓绘暟閲?
        if quantity_column_name not in sales_df.columns:
            print(f"閿欒锛氬湪閿€鍞暟鎹腑鏈壘鍒伴鏈熺殑鏁伴噺鍒?'{quantity_column_name}' 鐢ㄤ簬閿€閲忋€傚彲鐢ㄥ垪锛歿sales_df.columns.tolist()}")
            return {'by_material': {}, 'total': {}}

        sales_df[quantity_column_name] = pd.to_numeric(sales_df[quantity_column_name], errors='coerce')
        # 鑰冭檻鏄惁闇€瑕佸垹闄ら攢閲忎负0鎴栬礋鏁扮殑璁板綍锛屾牴鎹笟鍔￠€昏緫鍐冲畾
        sales_df = sales_df.dropna(subset=[quantity_column_name])  # 鍒犻櫎涓绘暟閲忎负NaN鐨勮
        # sales_df = sales_df[sales_df[quantity_column_name] > 0] # 渚嬪锛氬鏋滈攢閲忓繀椤讳负姝?        print(f'浣跨敤"{quantity_column_name}"浣滀负閿€閲忥紝骞惰繘琛屾暟鍊艰浆鎹㈠拰NaN鎺掗櫎鍚庯紝鍓╀綑 {len(sales_df)} 鏉¤褰?)
        
        # 鏃ユ湡鍒嗙粍锛岃绠楁瘡鏃ラ攢鍞暟鎹?        daily_sales = {}
        daily_total_sales = {}
        
        # 鎸夋棩鏈熷拰鍝佸悕鍒嗙粍 - 浣跨敤淇鍚庣殑鏃ユ湡鍒楀悕鍜岀墿鏂欏悕绉板垪鍚?        material_column_name = '鐗╂枡鍚嶇О'
        if material_column_name not in sales_df.columns:
            print(f"閿欒锛氬湪閿€鍞暟鎹腑鏈壘鍒伴鏈熺殑鐗╂枡鍒?'{material_name_column}'銆傚彲鐢ㄥ垪锛歿sales_df.columns.tolist()}")
            return {'by_material': {}, 'total': {}} # 杩斿洖绌?        
        grouped = sales_df.groupby([date_column_name, material_column_name])
        
        for (date, name), group in grouped:
            # 纭繚鏃ユ湡鏄?Timestamp 瀵硅薄锛屽鏋滈渶瑕佽浆鎹㈠洖瀛楃涓叉垨鍏朵粬鏍煎紡鍙互鍦ㄨ繖閲屽鐞?            # date 鍙橀噺鐜板湪鏄?'鍙戠エ鏃ユ湡' 鍒楃殑鍊?            # 濡傛灉鍚庣画瀛楀吀鐨?key 闇€瑕佹槸鐗瑰畾鐨勬棩鏈熸牸寮忥紝渚嬪 YYYY-MM-DD 瀛楃涓叉垨 date 瀵硅薄
            # 鍙互杩涜杞崲锛屼緥濡傦細 date_key = date.date() if isinstance(date, pd.Timestamp) else date
            if isinstance(date, pd.Timestamp):
                date_key = date.date() 
            else:
                 # 濡傛灉鍒嗙粍閿笉鏄?Timestamp (鐞嗚涓婁笉搴斿彂鐢燂紝浣嗕綔涓轰繚闄?, 灏濊瘯杞崲
                try:
                    date_key = pd.to_datetime(date).date()
                except: 
                    print(f"璀﹀憡锛氭棤娉曞皢鍒嗙粍閿?{date} 杞崲涓?date 瀵硅薄锛岃烦杩囨鏉＄洰銆?)
                    continue # 璺宠繃杩欎釜鏃犳硶澶勭悊鐨勬潯鐩?
            if date_key not in daily_sales:
                daily_sales[date_key] = {}
            
            # 绱姞鍚屼竴澶╁悓涓€鍝佸悕鐨勪富鏁伴噺
            total_quantity = group[quantity_column_name].sum()
            daily_sales[date_key][name] = total_quantity
            
            # 璁＄畻姣忔棩鎬婚攢閲?            if date_key not in daily_total_sales:
                daily_total_sales[date_key] = 0
            daily_total_sales[date_key] += total_quantity
        
        return {'by_material': daily_sales, 'total': daily_total_sales}
    
    def load_comprehensive_price_data(self, file_path=None):
        """
        鍔犺浇缁煎悎鍞环鏁版嵁 - 浠庣洰褰曚腑鏌ユ壘鏈€鏂扮殑缁煎悎鍞环X.XX.xlsx鏂囦欢
        
        鍙傛暟:
            file_path: 鍙€夛紝鐩存帴鎸囧畾鏂囦欢璺緞锛涘涓篘one鍒欒嚜鍔ㄦ煡鎵炬渶鏂版枃浠?            
        杩斿洖:
            str: 鎵惧埌鐨勭患鍚堝敭浠锋枃浠惰矾寰勶紝濡傛灉鏈壘鍒板垯杩斿洖None
        """
        import os
        import re
        import glob
        from datetime import datetime
        import config
        
        try:
            # 濡傛灉鎻愪緵浜嗗叿浣撴枃浠惰矾寰勶紝鍒欑洿鎺ヤ娇鐢?            if file_path is not None:
                print(f"浣跨敤鎸囧畾鐨勭患鍚堝敭浠锋枃浠? {file_path}")
                # 妫€鏌ユ枃浠舵槸鍚﹀瓨鍦?                if not os.path.exists(file_path):
                    print(f"閿欒: 鎸囧畾鐨勬枃浠朵笉瀛樺湪: {file_path}")
                    return None
                latest_file = file_path
            else:
                # 濡傛灉娌℃湁鎻愪緵鏂囦欢璺緞锛屽垯鍦ㄧ洰褰曚腑鏌ユ壘鏈€鏂扮殑缁煎悎鍞环X.XX.xlsx鏂囦欢
                directory = config.COMPREHENSIVE_PRICE_DIR
                pattern = config.COMPREHENSIVE_PRICE_PATTERN
                
                print(f"鍦ㄧ洰褰?{directory} 涓煡鎵惧尮閰嶆ā寮?{pattern} 鐨勬渶鏂扮患鍚堝敭浠锋枃浠?)
                
                # 鑾峰彇鎵€鏈夊尮閰嶇殑鏂囦欢
                all_files = []
                search_pattern = os.path.join(directory, "缁煎悎鍞环*.xlsx")
                for file_path in glob.glob(search_pattern):
                    file_name = os.path.basename(file_path)
                    match = re.search(pattern, file_name)
                    if match:
                        date_str = match.group(1)
                        try:
                            # 瑙ｆ瀽鏃ユ湡瀛楃涓?                            month, day = date_str.split('.')
                            # 浣跨敤褰撳墠骞翠唤
                            year = datetime.now().year
                            file_date = datetime(year, int(month), int(day))
                            all_files.append((file_path, file_date))
                        except ValueError:
                            print(f"鏃犳硶瑙ｆ瀽鏂囦欢鍚嶄腑鐨勬棩鏈? {file_name}")
                
                if not all_files:
                    print(f"閿欒: 鍦ㄧ洰褰?{directory} 涓病鏈夋壘鍒板尮閰嶇殑缁煎悎鍞环鏂囦欢")
                    return None
                
                # 鎸夋棩鏈熸帓搴忥紝鑾峰彇鏈€鏂扮殑鏂囦欢
                all_files.sort(key=lambda x: x[1], reverse=True)
                latest_file = all_files[0][0]
                print(f"鎵惧埌鏈€鏂扮殑缁煎悎鍞环鏂囦欢: {latest_file}")
            
            # 鐩存帴杩斿洖鏂囦欢璺緞锛屼笉鍐嶅鐞咵xcel鏁版嵁
            return latest_file
            
        except Exception as e:
            print(f"鍔犺浇缁煎悎鍞环鏁版嵁鏃跺嚭閿? {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def load_industry_price_data(self, chicken_path=None, raw_chicken_path=None, breast_path=None, leg_path=None):
        """
        鍔犺浇鍗撳垱璧勮鍘嗗彶浠锋牸鏁版嵁
        
        鍙傛暟:
            chicken_path: 楦¤嫍鍘嗗彶浠锋牸Excel鏂囦欢璺緞锛岃嫢涓篘one鍒欎娇鐢ㄩ厤缃枃浠朵腑鐨勮矾寰?            raw_chicken_path: 姣涢浮鍘嗗彶浠锋牸Excel鏂囦欢璺緞锛岃嫢涓篘one鍒欎娇鐢ㄩ厤缃枃浠朵腑鐨勮矾寰?            breast_path: 鏉垮喕澶ц兏鍘嗗彶浠锋牸Excel鏂囦欢璺緞锛岃嫢涓篘one鍒欎娇鐢ㄩ厤缃枃浠朵腑鐨勮矾寰?            leg_path: 鐞电惗鑵垮巻鍙蹭环鏍糆xcel鏂囦欢璺緞锛岃嫢涓篘one鍒欎娇鐢ㄩ厤缃枃浠朵腑鐨勮矾寰?            
        杩斿洖:
            dict: 鍖呭惈鍚勪骇鍝佷环鏍兼暟鎹殑瀛楀吀锛屾牸寮忎负 {浜у搧鍚? DataFrame}
        """
        import config
        
        # 浣跨敤閰嶇疆鏂囦欢涓殑璺緞锛堝鏋滄湭鎻愪緵锛?        chicken_path = chicken_path or config.CHICKEN_PRICE_PATH
        raw_chicken_path = raw_chicken_path or config.RAW_CHICKEN_PRICE_PATH
        breast_path = breast_path or config.BREAST_PRICE_PATH
        leg_path = leg_path or config.LEG_PRICE_PATH
        
        print(f"楦¤嫍璺緞: {chicken_path}")
        print(f"姣涢浮璺緞: {raw_chicken_path}")
        print(f"鏉垮喕澶ц兏璺緞: {breast_path}")
        print(f"鐞电惗鑵胯矾寰? {leg_path}")
        
        industry_data = {}
        
        # 鐢ㄤ簬澶勭悊Excel鏂囦欢鐨勯€氱敤鏂规硶
        def process_price_file(file_path, product_name, fallback_filename):
            try:
                if os.path.exists(file_path):
                    print(f"姝ｅ湪鍔犺浇{product_name}鍘嗗彶浠锋牸鏁版嵁: {file_path}")
                    try:
                        # 灏濊瘯璇诲彇Excel鏂囦欢
                        df = pd.read_excel(file_path, engine='openpyxl')
                        # 妫€鏌ュ垪鏁帮紝濡傛灉鍙湁灏戞暟鍑犲垪锛屽彲鑳芥槸甯歌鏍煎紡
                        if len(df.columns) < 9:
                            # 鏍囧噯鏍煎紡: 鐩存帴璇诲彇鏃ユ湡鍜屼环鏍煎垪
                            if 'date' not in df.columns and df.columns[0] != 'date':
                                df.rename(columns={df.columns[0]: 'date'}, inplace=True)
                            if 'price' not in df.columns and '浠锋牸' in df.columns:
                                df.rename(columns={'浠锋牸': 'price'}, inplace=True)
                        else:
                            # 鐗规畩鏍煎紡: 绗竴鍒楁槸鏃ユ湡锛岀涔濆垪鏄环鏍?                            print(f"{product_name}鏂囦欢浣跨敤鐗规畩鏍煎紡: 绗竴鍒椾负鏃ユ湡锛岀涔濆垪涓轰环鏍?)
                            if len(df.columns) >= 9:
                                # 鍒涘缓鏂扮殑DataFrame锛屽彧淇濈暀闇€瑕佺殑涓ゅ垪
                                df = pd.DataFrame({
                                    'date': df.iloc[:, 0],  # 绗竴鍒椾綔涓篸ate
                                    'price': df.iloc[:, 8]  # 绗節鍒椾綔涓簆rice
                                })
                            else:
                                print(f"璀﹀憡: {product_name}鏂囦欢鍒楁暟涓嶈冻锛屾棤娉曟彁鍙栦环鏍兼暟鎹?)
                                return None
                    except Exception as e1:
                        print(f"浣跨敤openpyxl寮曟搸鍔犺浇澶辫触锛屽皾璇曚娇鐢▁lrd寮曟搸: {str(e1)}")
                        try:
                            df = pd.read_excel(file_path, engine='xlrd')
                            # 鍚屾牱澶勭悊鍒?                            if len(df.columns) < 9:
                                if 'date' not in df.columns and df.columns[0] != 'date':
                                    df.rename(columns={df.columns[0]: 'date'}, inplace=True)
                                if 'price' not in df.columns and '浠锋牸' in df.columns:
                                    df.rename(columns={'浠锋牸': 'price'}, inplace=True)
                            else:
                                if len(df.columns) >= 9:
                                    df = pd.DataFrame({
                                        'date': df.iloc[:, 0],
                                        'price': df.iloc[:, 8]
                                    })
                                else:
                                    print(f"璀﹀憡: {product_name}鏂囦欢鍒楁暟涓嶈冻锛屾棤娉曟彁鍙栦环鏍兼暟鎹?)
                                    return None
                        except Exception as e2:
                            print(f"浣跨敤xlrd寮曟搸鍔犺浇澶辫触: {str(e2)}")
                            # 鏈€鍚庡皾璇曚娇鐢≒ython鐩存帴璇诲彇鏂囦欢
                            current_dir = os.path.dirname(os.path.abspath(__file__))
                            relative_path = os.path.join(current_dir, fallback_filename)
                            print(f"灏濊瘯浠庨粯璁よ矾寰勫姞杞? {relative_path}")
                            try:
                                df = pd.read_excel(relative_path, engine='openpyxl')
                                # 鍚屾牱澶勭悊鍒?                                if len(df.columns) < 9:
                                    if 'date' not in df.columns and df.columns[0] != 'date':
                                        df.rename(columns={df.columns[0]: 'date'}, inplace=True)
                                    if 'price' not in df.columns and '浠锋牸' in df.columns:
                                        df.rename(columns={'浠锋牸': 'price'}, inplace=True)
                                else:
                                    if len(df.columns) >= 9:
                                        df = pd.DataFrame({
                                            'date': df.iloc[:, 0],
                                            'price': df.iloc[:, 8]
                                        })
                                    else:
                                        print(f"璀﹀憡: {product_name}鏂囦欢鍒楁暟涓嶈冻锛屾棤娉曟彁鍙栦环鏍兼暟鎹?)
                                        return None
                            except Exception as e3:
                                print(f"灏濊瘯浠庨粯璁よ矾寰勫姞杞藉け璐? {str(e3)}")
                                return None
                    
                    # 妫€鏌ユ槸鍚︽湁蹇呰鐨勫垪
                    if 'date' in df.columns and 'price' in df.columns:
                        # 纭繚date鍒楁槸datetime鏍煎紡
                        df['date'] = pd.to_datetime(df['date'], errors='coerce')
                        # 纭繚price鍒楁槸鏁板€肩被鍨?                        df['price'] = pd.to_numeric(df['price'], errors='coerce')
                        # 娓呯悊鏁版嵁
                        df = df.dropna(subset=['date', 'price'])
                        return df
                    else:
                        print(f"璀﹀憡: {product_name}浠锋牸鏁版嵁缂哄皯蹇呰鐨勫垪銆傛枃浠朵腑鐨勫垪: {list(df.columns)}")
                        return None
                else:
                    print(f"璀﹀憡: {product_name}浠锋牸鏂囦欢涓嶅瓨鍦? {file_path}")
                    return None
            except Exception as e:
                print(f"鍔犺浇{product_name}浠锋牸鏁版嵁鏃跺嚭閿? {str(e)}")
                import traceback
                traceback.print_exc()
                return None
        
        # 鍔犺浇楦¤嫍浠锋牸鏁版嵁
        chicken_df = process_price_file(chicken_path, "楦¤嫍", "楦¤嫍鍘嗗彶浠锋牸.xlsx")
        if chicken_df is not None:
            industry_data['楦¤嫍'] = chicken_df
            print(f"鎴愬姛鍔犺浇楦¤嫍浠锋牸鏁版嵁锛屽叡 {len(chicken_df)} 鏉¤褰?)
        
        # 鍔犺浇姣涢浮浠锋牸鏁版嵁
        raw_chicken_df = process_price_file(raw_chicken_path, "姣涢浮", "姣涢浮鍘嗗彶浠锋牸.xlsx")
        if raw_chicken_df is not None:
            industry_data['姣涢浮'] = raw_chicken_df
            print(f"鎴愬姛鍔犺浇姣涢浮浠锋牸鏁版嵁锛屽叡 {len(raw_chicken_df)} 鏉¤褰?)
        
        # 鍔犺浇鏉垮喕澶ц兏浠锋牸鏁版嵁
        breast_df = process_price_file(breast_path, "鏉垮喕澶ц兏", "鏉垮喕澶ц兏鍘嗗彶浠锋牸.xlsx")
        if breast_df is not None:
            industry_data['鏉垮喕澶ц兏'] = breast_df
            print(f"鎴愬姛鍔犺浇鏉垮喕澶ц兏浠锋牸鏁版嵁锛屽叡 {len(breast_df)} 鏉¤褰?)
        
        # 鍔犺浇鐞电惗鑵夸环鏍兼暟鎹?        leg_df = process_price_file(leg_path, "鐞电惗鑵?, "鐞电惗鑵垮巻鍙蹭环鏍?xlsx")
        if leg_df is not None:
            industry_data['鐞电惗鑵?] = leg_df
            print(f"鎴愬姛鍔犺浇鐞电惗鑵夸环鏍兼暟鎹紝鍏?{len(leg_df)} 鏉¤褰?)
        
        # 娣诲姞鍙樺姩鍒楋紙濡傛灉涓嶅瓨鍦級
        for product, df in industry_data.items():
            if 'change' not in df.columns:
                # 鎸夋棩鏈熸帓搴?                df = df.sort_values(by='date')
                # 璁＄畻鍙樺姩
                df['change'] = df['price'].diff()
                industry_data[product] = df
        
        print(f"鏈€缁堣繑鍥炵殑industry_data鍖呭惈閿? {list(industry_data.keys())}")
        return industry_data 