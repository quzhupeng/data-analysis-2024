# -*- coding: utf-8 -*-
"""
鏁版嵁鍒嗘瀽妯″潡锛屽寘鍚环鏍兼尝鍔ㄥ垎鏋愮殑鏍稿績閫昏緫
"""

import pandas as pd
import numpy as np
from datetime import datetime

import config


class PriceAnalyzer:
    """浠锋牸鍒嗘瀽绫?""
    
    def __init__(self, all_data, sales_data=None, industry_trend_data=None, daily_production_data=None):
        """
        鍒濆鍖栦环鏍煎垎鏋愬櫒
        
        鍙傛暟:
            all_data: 浠锋牸鏁版嵁
            sales_data: 閿€鍞暟鎹?            industry_trend_data: 琛屼笟瓒嬪娍鏁版嵁
            daily_production_data: 姣忔棩浜ч噺鏁版嵁
        """
        self.all_data = all_data
        self.sales_data = sales_data
        self.industry_trend_data = industry_trend_data
        self.daily_production_data = daily_production_data
        
        # 鍒濆鍖栧垎鏋愮粨鏋?        self.abnormal_changes = []
        self.inconsistent_records = []
        self.conflict_records = []
        self.product_sales_ratio_data = None
    
    def analyze_price_changes(self):
        """鍒嗘瀽浠锋牸娉㈠姩鎯呭喌"""
        if self.all_data.empty:
            print("娌℃湁鏁版嵁鍙緵鍒嗘瀽")
            return
        
        print("寮€濮嬪垎鏋愪环鏍兼尝鍔?..")
        
        # 鎸夊搧鍚嶃€佽鏍煎拰鏃ユ湡鎺掑簭
        self.all_data.sort_values(['鍝佸悕', '瑙勬牸', '鏃ユ湡', '璋冧环娆℃暟'], inplace=True)
        
        # 璁＄畻浠锋牸鍙樺姩锛堢畝鍖栭€昏緫锛屽彧淇濈暀浠锋牸宸紓锛?        self.all_data['浠锋牸鍙樺姩'] = self.all_data['浠锋牸'] - self.all_data['鍓嶄环鏍?]
        
        # 浠锋牸宸紓闃堝€?        price_diff_threshold = 200  # 璁剧疆浠锋牸宸紓闃堝€间负200鍏?鍚?        
        # 璁＄畻浠锋牸宸紓鐨勭粷瀵瑰€?        self.all_data['浠锋牸宸紓缁濆鍊?] = self.all_data['浠锋牸鍙樺姩'].abs()
        
        # 绛涢€夊嚭浠锋牸宸紓缁濆鍊艰秴杩囬槇鍊肩殑璁板綍
        significant_records = self.all_data[self.all_data['浠锋牸宸紓缁濆鍊?] >= price_diff_threshold]
        
        # 妫€鏌ユ槸鍚︽湁绗﹀悎鏉′欢鐨勮褰?        if not significant_records.empty:
            # 鎻愬彇鎵€闇€鐨勫瓧娈碉紝骞舵坊鍔犱环鏍煎樊寮?            self.conflict_records = significant_records[
                ['鏃ユ湡', '鍝佸悕', '瑙勬牸', '璋冧环娆℃暟', '浠锋牸', '鍓嶄环鏍?]].copy()
            
            # 娣诲姞浠锋牸宸紓鍒?            self.conflict_records['浠锋牸宸紓'] = significant_records['浠锋牸鍙樺姩']
            
            # 杞崲涓哄瓧鍏稿垪琛?            self.conflict_records = self.conflict_records.to_dict('records')
            
            print(f"鍙戠幇 {len(self.conflict_records)} 鏉′环鏍煎樊寮傜粷瀵瑰€尖墺{price_diff_threshold}鐨勮褰?)
        else:
            self.conflict_records = []
            print(f"鏈彂鐜颁环鏍煎樊寮傜粷瀵瑰€尖墺{price_diff_threshold}鐨勮褰?)
        
        # 浠ヤ笅涓虹┖鍒楄〃锛屽洜涓烘垜浠笉鍐嶆娴嬭繖涓ら」
        self.abnormal_changes = []
        self.inconsistent_records = []
    
    def process_sales_data(self):
        """澶勭悊閿€鍞暟鎹紝鎸夋棩鏈熷垎缁?""
        if self.sales_data is None or self.sales_data.empty:
            print("娌℃湁閿€鍞暟鎹彲渚涘鐞?)
            return None
        
        try:
            # 鎸夋棩鏈熷垎缁?            daily_sales = {}
            
            # 纭繚鏃ユ湡鍒楁槸鏃ユ湡绫诲瀷
            # self.sales_data['鍙戠エ鏃ユ湡'] = pd.to_datetime(self.sales_data['鍙戠エ鏃ユ湡'])
            # ^^^ This is now handled in load_sales_data, assuming '鍙戠エ鏃ユ湡' is the correct date column name.
            # If not, ensure the correct date column from the loaded self.sales_data is used here.
            date_column_for_grouping = '鍙戠エ鏃ユ湡' # Match the one used in load_sales_data
            if date_column_for_grouping not in self.sales_data.columns:
                print(f"閿欒锛歱rocess_sales_data 鏈熸湜鐨勬棩鏈熷垪 '{date_column_for_grouping}' 涓嶅湪 self.sales_data 涓€?)
                return None

            # 妫€鏌ュ繀瑕佺殑鍒楁槸鍚﹀瓨鍦?(鐗╂枡鍚嶇О, 鏈竵鏃犵◣閲戦, 涓绘暟閲?
            # '涓绘暟閲? is now the fixed quantity column.
            required_columns = ['鐗╂枡鍚嶇О', '鏈竵鏃犵◣閲戦', '涓绘暟閲?]
            missing_columns = [col for col in required_columns if col not in self.sales_data.columns]
            
            if missing_columns:
                print(f"澶勭悊閿€鍞暟鎹椂缂哄皯蹇呰鐨勫垪: {', '.join(missing_columns)}")
                print(f"self.sales_data 涓殑鍙敤鍒楀悕: {self.sales_data.columns.tolist()}")
                return None
            
            # 鍥哄畾浣跨敤 '涓绘暟閲? 浣滀负鏁伴噺鍒?            quantity_column = '涓绘暟閲?
            print(f"process_sales_data 鍥哄畾浣跨敤 '{quantity_column}' 浣滀负鏁伴噺鍒椼€?)

            # 纭繚 '涓绘暟閲? 鍒楁槸鏁板€肩被鍨?(this should have been handled by load_sales_data)
            # Adding a check here for robustness before aggregation.
            if not pd.api.types.is_numeric_dtype(self.sales_data[quantity_column]):
                print(f"璀﹀憡: '{quantity_column}' 鍒楀湪浼犲叆 process_sales_data 鏃朵笉鏄暟鍊肩被鍨嬨€傚皾璇曡浆鎹?..")
                self.sales_data[quantity_column] = pd.to_numeric(self.sales_data[quantity_column], errors='coerce')
                # Potentially dropna again if conversion creates new NaNs, though load_sales_data should handle this.
                # self.sales_data = self.sales_data.dropna(subset=[quantity_column])
            
            # 鎸夋棩鏈熷垎缁?            for date_group_key, group in self.sales_data.groupby(self.sales_data[date_column_for_grouping].dt.date):
                # 閫夋嫨闇€瑕佺殑鍒?(鐗╂枡鍚嶇О, 鏈竵鏃犵◣閲戦, 涓绘暟閲?
                # Ensure we copy to avoid SettingWithCopyWarning if group is modified later for '鍚◣鍗曚环'
                group_for_processing = group[['鐗╂枡鍚嶇О', '鏈竵鏃犵◣閲戦', quantity_column]].copy()
                
                # 璁＄畻鏃ラ攢鍞€婚
                daily_total_amount = group_for_processing['鏈竵鏃犵◣閲戦'].sum()
                
                # 璁＄畻鏃ラ攢閲?(鏉ヨ嚜 '涓绘暟閲?)
                daily_volume = group_for_processing[quantity_column].sum()
                
                # 璁＄畻鏃ュ潎浠?(鍏?鍚?
                daily_avg_price = None
                if daily_volume > 0: # Avoid division by zero
                    # Formula: 閲戦 / 閿€閲?kg) * 1.09 * 1000 = 鍏?鍚?(鍚◣)
                    # Assuming '鏈竵鏃犵◣閲戦' and '涓绘暟閲? (in KG)
                    daily_avg_price = (daily_total_amount / daily_volume) * 1.09 * 1000
                
                # 璁＄畻姣忎釜浜у搧鐨勫惈绋庡崟浠?(based on '涓绘暟閲?)
                # Add '鍚◣鍗曚环' to group_for_processing to avoid modifying original 'group' slice if not needed elsewhere
                mask = group_for_processing[quantity_column] > 0
                group_for_processing.loc[mask, '鍚◣鍗曚环'] = (group_for_processing.loc[mask, '鏈竵鏃犵◣閲戦'] / 
                                                          group_for_processing.loc[mask, quantity_column]) * 1.09 * 1000
                group_for_processing.loc[~mask, '鍚◣鍗曚环'] = None # Set to None or np.nan where quantity is 0 or less
                
                # 鎸夌墿鏂欏悕绉版眹鎬?(閲戦鍜岄攢閲?
                summary_agg_dict = {
                    '鏈竵鏃犵◣閲戦': 'sum',
                    quantity_column: 'sum' # Aggregate '涓绘暟閲?
                }
                # Only add '鍚◣鍗曚环' to groupby if it was successfully calculated
                # For simplicity, we calculate mean of (potentially sparse) '鍚◣鍗曚环' after primary aggregation

                summary = group_for_processing.groupby('鐗╂枡鍚嶇О', as_index=False).agg(summary_agg_dict)
                
                # 璁＄畻骞舵槧灏勫钩鍧囧惈绋庡崟浠?(mean of individual product unit prices for that day)
                if '鍚◣鍗曚环' in group_for_processing.columns:
                    avg_prices_per_material = group_for_processing.groupby('鐗╂枡鍚嶇О')['鍚◣鍗曚环'].mean()
                    summary = summary.merge(avg_prices_per_material.rename('鍚◣鍗曚环'), on='鐗╂枡鍚嶇О', how='left')
                
                # 瀛樺偍鍒板瓧鍏镐腑
                daily_sales[date_group_key] = {
                    'data': summary, # DataFrame with '鐗╂枡鍚嶇О', '鏈竵鏃犵◣閲戦', '涓绘暟閲?, '鍚◣鍗曚环'
                    'total_amount': daily_total_amount,
                    'volume': daily_volume, # This is total daily sales from '涓绘暟閲?
                    'avg_price': daily_avg_price, # Overall daily average price
                    'quantity_column': quantity_column, # Name of the quantity column used ('涓绘暟閲?)
                    'product_count': len(summary)
                }
            
            return daily_sales
        
        except Exception as e:
            print(f"澶勭悊閿€鍞暟鎹椂鍑洪敊: {str(e)}")
            import traceback
            traceback.print_exc()  # 鎵撳嵃璇︾粏鐨勯敊璇爢鏍?            return None
    
    def calculate_production_sales_ratio(self, sales_data, production_data):
        """璁＄畻姣忔棩浜ч攢鐜?""
        import pandas as pd
        
        # 娣诲姞鏁版嵁绫诲瀷妫€鏌ュ拰杞崲
        print(f"calculate_production_sales_ratio - sales_data绫诲瀷: {type(sales_data)}")
        print(f"calculate_production_sales_ratio - production_data绫诲瀷: {type(production_data)}")
        
        if sales_data is None or production_data is None:
            print("璀﹀憡: 鏃犳硶璁＄畻浜ч攢鐜囷紝閿€鍞暟鎹垨鐢熶骇鏁版嵁涓虹┖")
            return {}
        
        print("璁＄畻浜ч攢鐜?..")
        
        # 妫€鏌ales_data瀛楁
        print(f"閿€鍞暟鎹垪: {list(sales_data.columns)}")
        
        # 纭畾鏃ユ湡鍒楀悕绉?        sales_date_column = None
        for column in ['date', '鍙戠エ鏃ユ湡', '鏃ユ湡']:
            if column in sales_data.columns:
                sales_date_column = column
                print(f"鎵惧埌閿€鍞暟鎹棩鏈熷垪: '{sales_date_column}'")
                break
        
        # 濡傛灉娌℃湁鎵惧埌鏃ユ湡鍒楋紝灏濊瘯鐚滄祴鍚?鏃ユ湡"鐨勫垪
        if not sales_date_column:
            for column in sales_data.columns:
                if '鏃ユ湡' in column or 'date' in column.lower():
                    sales_date_column = column
                    print(f"浣跨敤閿€鍞暟鎹垪: '{sales_date_column}' 浣滀负鏃ユ湡鍒?)
                    break
        
        if not sales_date_column:
            print("閿欒: 閿€鍞暟鎹腑鎵句笉鍒版棩鏈熷垪")
            return {}
        
        # 妫€鏌roduction_data瀛楁
        print(f"鐢熶骇鏁版嵁鍒? {list(production_data.columns)}")
        
        # 纭畾鐢熶骇鏁版嵁鏃ユ湡鍒楀悕绉?        production_date_column = None
        for column in ['date', '鍏ュ簱鏃ユ湡', '鏃ユ湡']:
            if column in production_data.columns:
                production_date_column = column
                print(f"鎵惧埌鐢熶骇鏁版嵁鏃ユ湡鍒? '{production_date_column}'")
                break
        
        # 濡傛灉娌℃湁鎵惧埌鏃ユ湡鍒楋紝灏濊瘯鐚滄祴鍚?鏃ユ湡"鐨勫垪
        if not production_date_column:
            for column in production_data.columns:
                if '鏃ユ湡' in column or 'date' in column.lower():
                    production_date_column = column
                    print(f"浣跨敤鐢熶骇鏁版嵁鍒? '{production_date_column}' 浣滀负鏃ユ湡鍒?)
                    break
        
        if not production_date_column:
            print("閿欒: 鐢熶骇鏁版嵁涓壘涓嶅埌鏃ユ湡鍒?)
            return {}
        
        # 纭繚鏃ユ湡鍒楁槸鏃ユ湡绫诲瀷
        sales_data[sales_date_column] = pd.to_datetime(sales_data[sales_date_column], errors='coerce')
        production_data[production_date_column] = pd.to_datetime(production_data[production_date_column], errors='coerce')
        
        # 鑾峰彇閿€鍞噺鍒楀悕
        quantity_column = None
        for col in ['閿€閲?, '涓绘暟閲?, '鏁伴噺']:
            if col in sales_data.columns:
                quantity_column = col
                break
        
        if not quantity_column:
            print("璀﹀憡: 鏈壘鍒伴攢鍞噺鍒楋紝鏃犳硶璁＄畻浜ч攢鐜?)
            return {}
        
        # 鑾峰彇鐢熶骇閲忓垪鍚?        production_column = None
        for col in ['浜ч噺', '鍏ュ簱鏁伴噺', '涓绘暟閲?]:
            if col in production_data.columns:
                production_column = col
                break
        
        if not production_column:
            print("璀﹀憡: 鏈壘鍒扮敓浜ч噺鍒楋紝鏃犳硶璁＄畻浜ч攢鐜?)
            return {}
        
        # 鎸夋棩鏈熷垎缁勮绠楅攢鍞噺
        daily_sales = {}
        try:
            sales_grouped = sales_data.groupby(sales_data[sales_date_column].dt.date)[quantity_column].sum()
            
            for date, sales_volume in sales_grouped.items():
                daily_sales[date] = sales_volume
            
            print(f"鎴愬姛璁＄畻 {len(daily_sales)} 澶╃殑閿€鍞噺")
        except Exception as e:
            print(f"璀﹀憡: 璁＄畻姣忔棩閿€鍞噺鏃跺彂鐢熼敊璇? {e}")
            import traceback
            traceback.print_exc()
            return {}
        
        # 鎸夋棩鏈熷垎缁勮绠楃敓浜ч噺
        daily_production = {}
        try:
            production_grouped = production_data.groupby(production_data[production_date_column].dt.date)[production_column].sum()
            
            for date, production_volume in production_grouped.items():
                daily_production[date] = production_volume
            
            print(f"鎴愬姛璁＄畻 {len(daily_production)} 澶╃殑鐢熶骇閲?)
        except Exception as e:
            print(f"璀﹀憡: 璁＄畻姣忔棩鐢熶骇閲忔椂鍙戠敓閿欒: {e}")
            import traceback
            traceback.print_exc()
            return {}
        
        # 璁＄畻浜ч攢鐜?        production_sales_ratio = {}
        
        # 鑾峰彇鎵€鏈夊敮涓€鏃ユ湡
        all_dates = sorted(set(list(daily_sales.keys()) + list(daily_production.keys())))
        
        for date in all_dates:
            # 涓洪槻姝㈤櫎闆堕敊璇紝闇€瑕佹鏌ョ敓浜ч噺
            sales = daily_sales.get(date, 0)
            production = daily_production.get(date, 0)
            
            # 浣跨敤涓庝骇閿€鐜囨槑缁嗗崱鐗囩浉鍚岀殑璁＄畻鏂规硶锛氫骇閿€鐜?= 閿€閲?浜ч噺 脳 100%
            if production > 0:
                ratio = (sales / production) * 100
                
                # 澶勭悊寮傚父鍊硷紝閬垮厤鍥捐〃姣斾緥澶辫皟
                if ratio > 500:  # 璁剧疆涓婇檺闃堝€?                    print(f"璀﹀憡: {date} 鐨勪骇閿€鐜囧紓甯搁珮: {ratio:.2f}%锛屽皢琚檺鍒朵负500%")
                    ratio = 500
            else:
                ratio = 0
                if sales > 0:
                    print(f"璀﹀憡: {date} 鏈夐攢鍞絾鏃犵敓浜ц褰?)
            
            production_sales_ratio[date] = {
                'sales': sales,
                'production': production,
                'ratio': ratio
            }
            
        print(f"鎴愬姛璁＄畻 {len(production_sales_ratio)} 澶╃殑浜ч攢鐜囨暟鎹?)
        return production_sales_ratio
    
    def analyze_product_sales_ratio(self):
        """鍒嗘瀽姣忔棩浜у搧绾у埆鐨勪骇閿€鐜?""
        import pandas as pd
        
        # 娣诲姞璇︾粏璋冭瘯淇℃伅
        print("================= 寮€濮嬪垎鏋愪骇鍝佷骇閿€鐜囨槑缁?=================")
        print(f"sales_data绫诲瀷: {type(self.sales_data)}")
        print(f"daily_production_data绫诲瀷: {type(self.daily_production_data)}")
        
        # 璁板綍澶勭悊鐨勭粨鏋?        result = []
        
        # 鑾峰彇閿€鍞拰浜ч噺鏁版嵁
        sales_data = self.sales_data
        daily_production_data = self.daily_production_data
        
        # 妫€鏌ラ攢鍞暟鎹粨鏋?        if sales_data is None:
            print("璀﹀憡: 閿€鍞暟鎹负绌?)
            return []
        
        if isinstance(sales_data, pd.DataFrame):
            print("閿€鍞暟鎹槸DataFrame锛屼絾闇€瑕佸鐞嗘垚by_material鏍煎紡")
            # 杞崲閿€鍞暟鎹负by_material鏍煎紡
            try:
                # 纭繚鏈夋棩鏈熷垪鍜屾暟閲忓垪
                if '鍙戠エ鏃ユ湡' in sales_data.columns:
                    date_column = '鍙戠エ鏃ユ湡'
                else:
                    # 灏濊瘯鎵惧埌鏃ユ湡鍒?                    date_columns = [col for col in sales_data.columns if 'date' in col.lower() or '鏃ユ湡' in col]
                    if date_columns:
                        date_column = date_columns[0]
                        print(f"浣跨敤鍒?'{date_column}' 浣滀负鏃ユ湡鍒?)
                    else:
                        print("閿欒: 閿€鍞暟鎹腑娌℃湁鎵惧埌鏃ユ湡鍒?)
                        return []
                
                # 鏌ユ壘鏁伴噺鍒?                quantity_column = None
                for col in sales_data.columns:
                    if '鏁伴噺' in col or '閲嶉噺' in col or '鍏枻' in col or 'kg' in col.lower():
                        quantity_column = col
                        print(f"鎵惧埌鏁伴噺/閲嶉噺鍒? '{quantity_column}'")
                        break
                
                if not quantity_column:
                    print("閿欒: 閿€鍞暟鎹腑娌℃湁鎵惧埌鏁伴噺鍒?)
                    return []
                
                # 纭繚鏃ユ湡鍒楁槸鏃ユ湡绫诲瀷
                sales_data[date_column] = pd.to_datetime(sales_data[date_column], errors='coerce')
                
                # 鎸夋棩鏈熷拰鍝佸悕鍒嗙粍
                sales_by_material = {}
                
                for (date, name), group in sales_data.groupby([sales_data[date_column].dt.date, '鐗╂枡鍚嶇О']):
                    if date not in sales_by_material:
                        sales_by_material[date] = {}
                    
                    # 绱姞鍚屼竴澶╁悓涓€鍝佸悕鐨勬暟閲?                    sales_by_material[date][name] = group[quantity_column].sum()
                
                # 鍒涘缓绗﹀悎瑕佹眰鐨勫瓧鍏哥粨鏋?                by_material_dict = {'by_material': sales_by_material}
                sales_data = by_material_dict
                print(f"宸茶浆鎹㈤攢鍞暟鎹负by_material鏍煎紡锛屽寘鍚?{len(sales_by_material)} 澶╂暟鎹?)
            except Exception as e:
                print(f"杞崲閿€鍞暟鎹椂鍑洪敊: {e}")
                import traceback
                traceback.print_exc()
                return []
        elif not isinstance(sales_data, dict) or 'by_material' not in sales_data:
            print(f"璀﹀憡: 閿€鍞暟鎹牸寮忎笉鏄痓y_material瀛楀吀: {type(sales_data)}")
            return []
        
        # 杞崲鏁版嵁鏍煎紡纭繚绫诲瀷姝ｇ‘
        if isinstance(daily_production_data, dict) and 'by_material' in daily_production_data:
            production_by_material = daily_production_data['by_material']
            print(f"浜ч噺鏁版嵁姝ｇ‘锛屽寘鍚?{len(production_by_material)} 澶╂暟鎹?)
        else:
            print(f"璀﹀憡: 浜ч噺鏁版嵁鏍煎紡涓嶆纭? {type(daily_production_data)}")
            return []
        
        # 鏄剧ず閿€鍞暟鎹腑鐨勬棩鏈?        sales_by_material = sales_data['by_material']
        print(f"閿€鍞暟鎹棩鏈? {list(sales_by_material.keys())[:5]}...")
        print(f"浜ч噺鏁版嵁鏃ユ湡: {list(production_by_material.keys())[:5]}...")
        
        # 閬嶅巻姣忎竴澶╃殑鏁版嵁
        common_dates = set(sales_by_material.keys()) & set(production_by_material.keys())
        print(f"閿€鍞暟鎹拰浜ч噺鏁版嵁鍏辨湁 {len(common_dates)} 澶╅噸鍙?)
        
        for date in production_by_material:
            date_str = date.strftime("%Y-%m-%d") if hasattr(date, 'strftime') else str(date)
            print(f"澶勭悊鏃ユ湡: {date_str}")
            
            # 鑾峰彇褰撳ぉ浜ч噺鏁版嵁
            day_production = production_by_material[date]
            
            # 鑾峰彇褰撳ぉ閿€閲忔暟鎹?            day_sales = {}
            if date in sales_by_material:
                day_sales = sales_by_material[date]
            
            # 鍒涘缓浜у搧绾у埆浜ч攢鐜嘍ataFrame
            product_data = []
            
            # 鍚堝苟鎵€鏈変骇鍝?            all_products = set(day_production.keys()) | set(day_sales.keys())
            
            for product in all_products:
                # 鑾峰彇浜ч噺鍜岄攢閲?                production_qty = day_production.get(product, 0)
                sales_qty = day_sales.get(product, 0)
                
                # 璁＄畻浜ч攢鐜?                sales_ratio = (sales_qty / production_qty * 100) if production_qty > 0 else 0
                
                product_data.append({
                    '鍝佸悕': product,
                    '閿€閲?: sales_qty,
                    '浜ч噺': production_qty,
                    '浜ч攢鐜?: sales_ratio
                })
            
            # 鍒涘缓DataFrame
            if product_data:
                product_df = pd.DataFrame(product_data)
                result.append({
                    'date': date,
                    'data': product_df
                })
                print(f"娣诲姞浜嗘棩鏈?{date_str} 鐨勪骇閿€鐜囨暟鎹紝鍖呭惈 {len(product_data)} 涓骇鍝?)
            else:
                print(f"鏃ユ湡 {date_str} 娌℃湁鏈夋晥鐨勪骇鍝佷骇閿€鐜囨暟鎹?)
        
        print(f"鎬诲叡鐢熸垚浜?{len(result)} 澶╃殑浜у搧浜ч攢鐜囨槑缁嗘暟鎹?)
        print("================= 缁撴潫鍒嗘瀽浜у搧浜ч攢鐜囨槑缁?=================")
        return result
    
    def calculate_product_sales_ratio_detail(self, daily_sales_data, daily_production_data):
        """璁＄畻姣忔棩浜у搧浜ч攢鐜囨槑缁?""
        print("璁＄畻姣忔棩浜у搧浜ч攢鐜囨槑缁?..")
        
        daily_sales_by_material = daily_sales_data['by_material']
        daily_production_by_material = daily_production_data['by_material']
        
        product_sales_ratio_data = []
        
        # 鑾峰彇鎵€鏈夋棩鏈?        all_dates = sorted(set(list(daily_sales_by_material.keys()) + list(daily_production_by_material.keys())))
        
        for date in all_dates:
            sales_data = daily_sales_by_material.get(date, {})
            production_data = daily_production_by_material.get(date, {})
            
            # 鍚堝苟鎵€鏈変骇鍝?            all_products = set(list(sales_data.keys()) + list(production_data.keys()))
            
            # 涓烘瘡涓骇鍝佽绠椾骇閿€鐜?            product_data = []
            for product in all_products:
                sales = sales_data.get(product, 0)
                production = production_data.get(product, 0)
                
                # 璁＄畻浜ч攢鐜?- 淇敼鍚庣殑閫昏緫
                if production != 0:  # 鍙浜ч噺涓嶄负0锛屽氨璁＄畻浜ч攢鐜?                    ratio = (sales / production) * 100
                else:
                    ratio = 0  # 浜ч噺涓?鏃讹紝浜ч攢鐜囦负0
                
                product_data.append({
                    '鍝佸悕': product,
                    '閿€閲?: sales,
                    '浜ч噺': production,
                    '浜ч攢鐜?: ratio
                })
            
            # 鎸変骇閿€鐜囬檷搴忔帓搴?            if product_data:
                df = pd.DataFrame(product_data)
                df = df.sort_values(by=['浜ч攢鐜?], ascending=False)
                
                # 娣诲姞鍒扮粨鏋滃垪琛?                product_sales_ratio_data.append({
                    'date': date,
                    'data': df
                })
        
        print(f"璁＄畻浜?{len(product_sales_ratio_data)} 澶╃殑浜у搧浜ч攢鐜囨槑缁?)
        return product_sales_ratio_data 