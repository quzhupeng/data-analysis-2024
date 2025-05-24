# -*- coding: utf-8 -*-
"""
鐢熸垚閿€鍞儏鍐垫姤鍛婇〉闈?(sales.html)銆?
"""

import os
import pandas as pd
from html_utils import generate_header, generate_navigation, generate_footer, write_html_report, generate_image_tag
from collections import OrderedDict # 瀵煎叆OrderedDict

def _generate_sales_content(daily_sales, comprehensive_price_file, output_dir):
    """鐢熸垚閿€鍞儏鍐甸儴鍒嗙殑HTML鍐呭

    Args:
        daily_sales (dict): 姣忔棩閿€鍞暟鎹? {date: {'volume': v, 'avg_price': p, 'product_count': c, 'data': df, 'quantity_column': qc}}
        comprehensive_price_file (str): 缁煎悎鍞环Excel鏂囦欢璺緞
        output_dir (str): 杈撳嚭鐩綍

    Returns:
        str: 閿€鍞儏鍐甸儴鍒嗙殑HTML浠ｇ爜銆?
    """
    if not daily_sales or len(daily_sales) == 0:
        print("璀﹀憡: 姣忔棩閿€鍞暟鎹负绌猴紝璺宠繃閿€鍞儏鍐甸儴鍒嗙敓鎴?)
        return """
        <div class="section">
            <div class="section-header"><h2>閿€鍞儏鍐靛垎鏋?/h2></div>
            <div class="section-body"><p>鏃犻攢鍞暟鎹彲渚涙樉绀恒€?/p></div>
        </div>
        """

    html = '''
    <div class="section">
        <div class="section-header">
            <h2>閿€鍞儏鍐靛垎鏋?/h2>
        </div>
        <div class="section-body">
    '''

    # 娣诲姞缁煎悎鍞环琛ㄦ牸
    if comprehensive_price_file and os.path.exists(comprehensive_price_file):
        try:
            import pandas as pd
            import re
            
            file_name = os.path.basename(comprehensive_price_file)
            match = re.search(r"缁煎悎鍞环(\\d+\\.\\d+)\\.xlsx", file_name)
            date_str = match.group(1) if match else "鏈€鏂?
            
            print(f"澶勭悊缁煎悎鍞环鏂囦欢: {comprehensive_price_file}")
            df = pd.read_excel(comprehensive_price_file, header=None)
            
            explanation_text = ""
            for r_idx in range(len(df)):
                for c_idx in range(len(df.columns)):
                    cell_val = df.iloc[r_idx, c_idx]
                    if pd.notna(cell_val) and isinstance(cell_val, str) and "璇存槑" in cell_val:
                        explanation_text = cell_val if cell_val.startswith("璇存槑锛?) else "璇存槑锛? + cell_val
                        df.iloc[r_idx, c_idx] = "" 
                        break 
                if explanation_text: break
            
            if not explanation_text:
                explanation_text = "璇存槑锛氬姞宸ヤ竴浜屽巶瀹為檯涓猴細鍘绘瘺銆佽銆佽偁鍚庤皟鏁村姞宸ヤ骇鍝佷环鏍肩殑缁煎悎浠锋牸銆備笌鐪熷疄琛屼笟浠锋牸涔熺浉鐢氱浉绗︺€?
            
            html += f'''
            <div class="subsection">
                <h3>缁煎悎鍞环 ({date_str})</h3>
                <div class="table-responsive" id="comp-price-table-container">
                    <table class="table table-bordered table-striped price-table" style="text-align: center;">
            '''
            html += '''
            <style>
                .price-table th, .price-table td { text-align: center; vertical-align: middle; }
                .price-table th { background-color: #f2f2f2; font-weight: bold; }
                .price-table .price-category { background-color: #f0f4f8; font-weight: bold; }
                .price-table .price-value { text-align: right; font-family: Arial, sans-serif; }
                .empty-cell { background-color: #fafafa; }
                .calculation-method { background-color: #f5f5f5; font-weight: 500; }
                .swipe-hint { text-align: center; color: #666; font-size: 0.8em; padding: 5px; margin-bottom: 5px; }
            </style>
            '''
            
            html += "<thead>"
            html += '<tr><th colspan="3" style="background-color: #e6f2ff;">绫诲埆</th>'
            # 鏃ユ湡鍒楁爣棰?(浠庣4鍒楀埌鏈€鍚?鍒?
            for col_idx in range(3, len(df.columns)):
                header_val = df.iloc[1, col_idx] # 绗?琛屾槸鏃ユ湡/鍧囦环鏍囬
                html += f'<th style="background-color: #e6f2ff;">{str(header_val) if pd.notna(header_val) else ""}</th>'
            html += "</tr></thead>"
            
            html += "<tbody>"
            
            categories = OrderedDict()
            current_main_category_name = None
            current_main_category_last_calc_method = ""

            for r_idx in range(2, len(df)): # 浠嶦xcel鐨勭3琛屽紑濮嬫暟鎹?
                main_cat_val_raw = df.iloc[r_idx, 0]
                main_cat_val = str(main_cat_val_raw).strip() if pd.notna(main_cat_val_raw) else ""
                
                factory_val_raw = df.iloc[r_idx, 1]
                factory_val = str(factory_val_raw).strip() if pd.notna(factory_val_raw) else ""
                
                calc_method_val_raw = df.iloc[r_idx, 2]
                calc_method_val = str(calc_method_val_raw).strip() if pd.notna(calc_method_val_raw) else ""

                is_genuine_data_row = False
                if factory_val != "" or calc_method_val != "":
                    is_genuine_data_row = True
                else:
                    for c_idx_check in range(3, len(df.columns)):
                        if pd.notna(df.iloc[r_idx, c_idx_check]):
                            is_genuine_data_row = True
                            break
                if not is_genuine_data_row:
                    continue

                if main_cat_val != "":
                    current_main_category_name = main_cat_val
                    if current_main_category_name not in categories:
                        categories[current_main_category_name] = OrderedDict()
                    current_main_category_last_calc_method = "" 
                
                if current_main_category_name is None: continue

                effective_calc_method = calc_method_val
                if effective_calc_method == "":
                    effective_calc_method = current_main_category_last_calc_method
                else:
                    current_main_category_last_calc_method = effective_calc_method
                
                if effective_calc_method not in categories[current_main_category_name]:
                    categories[current_main_category_name][effective_calc_method] = []
                categories[current_main_category_name][effective_calc_method].append(r_idx)

            # 娓叉煋HTML琛ㄦ牸
            for main_cat_name, calc_methods_dict in categories.items():
                total_rows_for_main_cat = sum(len(idx_list) for idx_list in calc_methods_dict.values())
                if total_rows_for_main_cat == 0: continue

                is_first_html_row_for_main_cat = True
                
                avg_price_cell_html = ""
                # 纭畾鍧囦环鍒?(鏈€鍚庝竴鍒?
                avg_price_col_idx = len(df.columns) - 1
                if avg_price_col_idx >= 3: #纭繚鏈夊潎浠峰垪
                    # 浠庤繖涓富鍒嗙被鐨勭涓€涓疄闄呮暟鎹鑾峰彇鍧囦环
                    first_data_row_original_idx = -1
                    for _, row_idx_list_for_calc_method in calc_methods_dict.items():
                        if row_idx_list_for_calc_method:
                            first_data_row_original_idx = row_idx_list_for_calc_method[0]
                            break
                    
                    if first_data_row_original_idx != -1:
                        avg_price_val = df.iloc[first_data_row_original_idx, avg_price_col_idx]
                        cell_content = f"{int(avg_price_val):,}" if pd.notna(avg_price_val) and isinstance(avg_price_val, (int, float)) else (str(avg_price_val) if pd.notna(avg_price_val) else "")
                        avg_price_cell_html = f'<td rowspan="{total_rows_for_main_cat}" class="price-value { "empty-cell" if cell_content == "" else ""}">{cell_content}</td>'
                    else: # Should not happen if total_rows_for_main_cat > 0
                        avg_price_cell_html = f'<td rowspan="{total_rows_for_main_cat}" class="empty-cell"></td>'


                for calc_method_name, row_indices_list in calc_methods_dict.items():
                    rows_for_this_calc_method = len(row_indices_list)
                    if rows_for_this_calc_method == 0: continue

                    for i, current_row_original_idx in enumerate(row_indices_list):
                        html += "<tr>"
                        
                        if is_first_html_row_for_main_cat:
                            html += f'<td rowspan="{total_rows_for_main_cat}" class="price-category">{main_cat_name}</td>'
                        
                        factory_val_on_row = df.iloc[current_row_original_idx, 1]
                        html += f'<td>{str(factory_val_on_row) if pd.notna(factory_val_on_row) else ""}</td>'
                        
                        if i == 0: # First row for this specific calc_method_name group
                            html += f'<td rowspan="{rows_for_this_calc_method}" class="calculation-method { "empty-cell" if calc_method_name == "" else ""}">{calc_method_name}</td>'
                        
                        # 鏁版嵁鍊?(浠庣4鍒楀埌鍊掓暟绗?鍒?
                        for data_col_df_idx in range(3, len(df.columns) - 1):
                            data_val = df.iloc[current_row_original_idx, data_col_df_idx]
                            cell_content = f"{int(data_val):,}" if pd.notna(data_val) and isinstance(data_val, (int, float)) else (str(data_val) if pd.notna(data_val) else "")
                            html += f'<td class="price-value { "empty-cell" if cell_content == "" else ""}">{cell_content}</td>'
                        
                        if is_first_html_row_for_main_cat:
                            html += avg_price_cell_html
                        
                        html += "</tr>"
                        is_first_html_row_for_main_cat = False
            
            html += "</tbody>"
            html += '''
                    </table>
                </div>
                <div class="swipe-hint"><i class="bi bi-arrow-left-right"></i> 宸﹀彸婊戝姩鏌ョ湅鏇村</div>
                <div class="description">
                    <p style="text-align: left; font-size: 13px; color: #666; margin-top: 10px; border-left: 3px solid #1976D2; padding-left: 10px; background-color: #f9f9f9; padding: 8px;">
                        <strong>璇存槑锛?/strong>''' + explanation_text.replace("璇存槑锛?, "") + '''
                    </p>
                </div>
            </div>
            '''
        except Exception as e:
            print(f"澶勭悊缁煎悎鍞环鏂囦欢鏃跺嚭閿? {str(e)}")
            import traceback
            traceback.print_exc()
            html += f'<div class="subsection"><h3>缁煎悎鍞环</h3><p>鏃犳硶鍔犺浇缁煎悎鍞环鏁版嵁: {str(e)}</p></div>'
    else:
        print(f"缁煎悎鍞环鏂囦欢鏈壘鍒版垨鏃犳晥: {comprehensive_price_file}")
        html += '<div class="subsection"><h3>缁煎悎鍞环</h3><p>鏈壘鍒扮患鍚堝敭浠锋暟鎹枃浠?/p></div>'

    # Add sales trend chart
    sales_trend_chart_filename = "daily_sales_trend.png"
    sales_trend_chart_path = os.path.join(output_dir, sales_trend_chart_filename)
    if os.path.exists(sales_trend_chart_path):
        html += f'''
        <div class="subsection">
            <h3>閿€鍞秼鍔?/h3>
            <div class="chart-container">
                 {generate_image_tag(sales_trend_chart_filename, alt_text="姣忔棩閿€閲忓拰瀹為檯閿€鍞潎浠疯秼鍔?, css_class="chart")}
            </div>
            <p style="text-align: right; font-size: 12px; color: #666; margin-top: 5px;">娉細閿€閲忓幓闄ゅ壇浜у搧鍜岄矞鍝侊紝閿€鍞潎浠蜂负瀹為檯鎬婚噾棰?鎬婚噸閲忓緱鍒扮殑鍚◣浠锋牸</p>
            <p style="text-align: right; font-size: 12px; color: #666; margin-top: 2px;">鏁版嵁鏉ユ簮锛氶攢鍞彂绁ㄦ墽琛屾煡璇紙鎺掗櫎瀹㈡埛鍚嶇О涓虹┖銆佸壇浜у搧銆侀矞鍝佺殑璁板綍锛?/p>
        </div>
        '''
    else:
        print(f"閿€鍞秼鍔垮浘鏈壘鍒? {sales_trend_chart_path}")


    html += '''
        <div class="subsection">
            <h3>閿€鍞槑缁?/h3>
            <p>姣忔棩鍚勪骇鍝佺殑璇︾粏閿€鍞暟鎹凡绉昏嚦璇︾粏鏁版嵁椤甸潰銆?/p>
            <p><a href="details.html#daily-sales-details" class="btn btn-primary">鐐瑰嚮鏌ョ湅姣忔棩鏄庣粏鏁版嵁</a></p>
            <p style="text-align: right; font-size: 12px; color: #666; margin-top: 5px;">鏁版嵁鏉ユ簮锛氶攢鍞彂绁ㄦ墽琛屾煡璇紙鎺掗櫎瀹㈡埛鍚嶇О涓虹┖銆佸壇浜у搧銆侀矞鍝佺殑璁板綍锛?/p>
        </div>
        </div> <!-- Close section-body -->
    </div> <!-- Close section -->
    '''
    return html

def generate_sales_page(daily_sales, comprehensive_price_file, output_dir):
    """鐢熸垚 sales.html 椤甸潰

    Args:
        daily_sales (dict): 姣忔棩閿€鍞暟鎹€?
        comprehensive_price_file (str): 缁煎悎鍞环鏂囦欢璺緞銆?
        output_dir (str): HTML 鏂囦欢杈撳嚭鐩綍銆?
    """
    print("寮€濮嬬敓鎴?sales.html 椤甸潰...")
    page_title = "鏄ラ洩椋熷搧鐢熷搧浜ч攢鍒嗘瀽鎶ュ憡 - 閿€鍞儏鍐?
    header_html = generate_header(title=page_title, output_dir=output_dir)
    nav_html = generate_navigation(active_page="sales")
    sales_content_html = _generate_sales_content(daily_sales, comprehensive_price_file, output_dir)
    footer_html = generate_footer()

    full_html = header_html + nav_html + sales_content_html + footer_html

    write_html_report(full_html, "sales.html", output_dir)

# # --- Example Usage (for testing) ---
# if __name__ == '__main__':
#     from datetime import datetime
#     # Create dummy data
#     dummy_sales_data = {
#         datetime(2023, 10, 25): {
#             'volume': 5000, 'avg_price': 15000, 'product_count': 3,
#             'quantity_column': '閿€鍞噺',
#             'data': pd.DataFrame({
#                 '鐗╂枡鍚嶇О': ['鍐婚浮鑵緼', '鍐婚浮鑳窧', '椴滈浮缈匔'],
#                 '閿€鍞噺': [2500, 1500, 1000],
#                 '鏈竵鏃犵◣閲戦': [30000, 25000, 20000],
#                 '鍚◣鍗曚环': [15000, 16000, 21000]
#             })
#         },
#         datetime(2023, 10, 26): {
#             'volume': 6200, 'avg_price': 15200, 'product_count': 2,
#             'quantity_column': '瀹為檯閲嶉噺',
#             'data': pd.DataFrame({
#                 '鐗╂枡鍚嶇О': ['鍐婚浮鑵緼', '椴滈浮缈匔'],
#                 '瀹為檯閲嶉噺': [4000, 2200],
#                 '鏈竵鏃犵◣閲戦': [48000, 44000],
#                 '鍚◣鍗曚环': [15100, 20500]
#             })
#         },
#          datetime(2023, 10, 27): {
#              'volume': 0, 'avg_price': None, 'product_count': 0,
#              'quantity_column': '閿€鍞噺',
#              'data': pd.DataFrame(columns=['鐗╂枡鍚嶇О', '閿€鍞噺', '鏈竵鏃犵◣閲戦', '鍚◣鍗曚环'])
#          }
#     }
#     dummy_comp_chart = "comprehensive_price_chart.png"

#     output_directory = './test_report_output'
#     os.makedirs(output_directory, exist_ok=True)
#     # Create dummy image files
#     try:
#         with open(os.path.join(output_directory, dummy_comp_chart), 'w') as f: f.write("comp price chart")
#         with open(os.path.join(output_directory, "daily_sales_trend.png"), 'w') as f: f.write("sales trend chart")
#     except OSError as e:
#         print(f"鏃犳硶鍒涘缓娴嬭瘯鍥剧墖: {e}")

#     generate_sales_page(dummy_sales_data, dummy_comp_chart, output_directory)
#     print(f"娴嬭瘯 sales.html 宸茬敓鎴愬湪 {output_directory}") 