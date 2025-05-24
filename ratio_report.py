# -*- coding: utf-8 -*-
"""
鐢熸垚浜ч攢鐜囧垎鏋愭姤鍛婇〉闈?(ratio.html)銆?"""

import os
import pandas as pd
from datetime import datetime
from html_utils import generate_header, generate_navigation, generate_footer, write_html_report, generate_image_tag

def _generate_product_sales_ratio_detail_panel(date_str, data):
    """鐢熸垚姣忔棩浜у搧浜ч攢鐜囨槑缁嗛潰鏉?(绉绘鑷師 _generate_product_sales_ratio_detail_panel)

    Args:
        date_str (str): 鏃ユ湡瀛楃涓?(YYYY-MM-DD).
        data (pd.DataFrame): 褰撴棩鐨勪骇鍝佷骇閿€鏄庣粏鏁版嵁銆?
    Returns:
        str: 鍗曚釜闈㈡澘鐨凥TML浠ｇ爜銆?    """
    # Add data validation check
    if data is None or data.empty:
        print(f"璀﹀憡: {date_str} 鐨勪骇鍝佷骇閿€鐜囨槑缁嗘暟鎹负绌猴紝璺宠繃璇ラ潰鏉跨敓鎴?)
        # Return an empty div or a message panel
        return f'''
        <div id="ratioPanel_{date_str}" class="ratio-panel" style="display: none;">
            <div class="ratio-panel-header">
                 <h4>浜ч攢鐜囨槑缁?- {date_str}</h4>
                 <button onclick="toggleRatioPanel('{date_str}', event)" class="close-button"><i class="bi bi-x-lg"></i></button>
            </div>
            <div class="ratio-panel-body"><p>褰撴棩鏃犺缁嗕骇鍝佷骇閿€鏁版嵁銆?/p></div>
        </div>
        '''

    panel_html = f'''
    <div id="ratioPanel_{date_str}" class="ratio-panel" style="display: none;">
        <div class="ratio-panel-header">
            <h4>浜ч攢鐜囨槑缁?- {date_str}</h4>
            <div class="ratio-panel-controls">
                <input type="text" id="ratioSearch_{date_str}" onkeyup="searchTableInPanel('ratio', '{date_str}')" placeholder="鎼滅储浜у搧..." class="search-input">
                <button onclick="toggleRatioPanel('{date_str}', event)" class="close-button">
                    <i class="bi bi-x-lg"></i>
                </button>
            </div>
        </div>
        <div class="ratio-panel-body">
            <div class="sales-table-container"> <!-- Reusing sales table container style -->
                <table id="ratioTable_{date_str}">
                    <thead>
                        <tr>
                            <th>浜у搧鍚嶇О</th>
                            <th>閿€閲?/th>
                            <th>浜ч噺</th>
                            <th>浜ч攢鐜?/th>
                        </tr>
                    </thead>
                    <tbody>
    '''

    # Sort data by '浜ч攢鐜? descending, handle potential errors
    try:
        # Ensure '浜ч攢鐜? column exists and is numeric before sorting
        if '浜ч攢鐜? in data.columns and pd.api.types.is_numeric_dtype(data['浜ч攢鐜?]):
            data_sorted = data.sort_values(by='浜ч攢鐜?, ascending=False, na_position='last')
        else:
            print(f"璀﹀憡: {date_str} 鐨?'浜ч攢鐜? 鍒椾笉瀛樺湪鎴栭潪鏁板€硷紝鏃犳硶鎺掑簭銆?)
            data_sorted = data # Use original data if sorting fails
    except Exception as e:
        print(f"鎺掑簭浜ч攢鐜囨槑缁嗘椂鍑洪敊 ({date_str}): {e}")
        data_sorted = data # Fallback to original data

    # Add product data rows
    required_cols = ['鍝佸悕', '閿€閲?, '浜ч噺', '浜ч攢鐜?]
    if not all(col in data_sorted.columns for col in required_cols):
         panel_html += "<tr><td colspan='4'>鏁版嵁鍒椾笉瀹屾暣銆?/td></tr>"
    else:
        for _, row in data_sorted.iterrows():
            # Safely get values
            prod_name = row.get('鍝佸悕', 'N/A')
            sales_val = row.get('閿€閲?)
            prod_val = row.get('浜ч噺')
            ratio_val = row.get('浜ч攢鐜?)

            # Format numeric values safely
            try:
                sales_display = f"{int(sales_val):,}" if pd.notna(sales_val) else "-"
            except (ValueError, TypeError):
                sales_display = str(sales_val)
            try:
                prod_display = f"{int(prod_val):,}" if pd.notna(prod_val) else "-"
            except (ValueError, TypeError):
                prod_display = str(prod_val)

            ratio_class = ""
            ratio_display = "-"
            if pd.notna(ratio_val):
                 try:
                     ratio_float = float(ratio_val)
                     ratio_display = f"{int(ratio_float)}%"
                     if ratio_float > 100:
                         ratio_class = "high-value" # Shortage
                     elif ratio_float < 90: # Adjusted threshold slightly for low value emphasis
                         ratio_class = "low-value"  # Surplus
                     # else: implicitly balanced, no class needed
                 except (ValueError, TypeError):
                      ratio_display = str(ratio_val) # Display as is if not convertible to float

            panel_html += f'''
                        <tr>
                            <td>{prod_name}</td>
                            <td class="text-right">{sales_display}</td>
                            <td class="text-right">{prod_display}</td>
                            <td class="{ratio_class} text-right">{ratio_display}</td>
                        </tr>
            '''

        # Calculate and add total row safely
        try:
            total_sales = data['閿€閲?].sum() if '閿€閲? in data.columns and pd.api.types.is_numeric_dtype(data['閿€閲?]) else 0
            total_production = data['浜ч噺'].sum() if '浜ч噺' in data.columns and pd.api.types.is_numeric_dtype(data['浜ч噺']) else 0
            total_ratio = (total_sales / total_production * 100) if total_production > 0 else 0

            total_ratio_class = ""
            if total_ratio > 100:
                total_ratio_class = "high-value"
            elif total_ratio < 90:
                total_ratio_class = "low-value"

            panel_html += f'''
                    <tr class="total-row">
                        <td><strong>鍚堣</strong></td>
                        <td class="text-right"><strong>{int(total_sales):,}</strong></td>
                        <td class="text-right"><strong>{int(total_production):,}</strong></td>
                        <td class="{total_ratio_class} text-right"><strong>{int(total_ratio)}%</strong></td>
                    </tr>
            '''
        except Exception as e:
            print(f"璁＄畻鍚堣琛屾椂鍑洪敊 ({date_str}): {e}")
            panel_html += "<tr><td colspan='4'>璁＄畻鍚堣鏃跺嚭閿欍€?/td></tr>"

    panel_html += '''
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    '''
    return panel_html

def _generate_product_sales_ratio_detail(product_sales_ratio_data):
    """鐢熸垚浜у搧浜ч攢鐜囨槑缁嗛儴鍒?(鍗＄墖 + 闈㈡澘) - MODIFIED: Only generates title and link.

    Args:
        product_sales_ratio_data (list): 鍖呭惈姣忔棩浜у搧鏄庣粏鏁版嵁鐨勫垪琛?(used only to check if data exists).

    Returns:
        str: 浜у搧浜ч攢鐜囨槑缁嗛儴鍒嗙殑HTML浠ｇ爜 (title + link or no data message).
    """
    # Check data validity
    if not product_sales_ratio_data or len(product_sales_ratio_data) == 0:
        print("璀﹀憡: 浜у搧浜ч攢鐜囨槑缁嗘暟鎹负绌猴紝璺宠繃鏄庣粏閮ㄥ垎鐢熸垚")
        return """
        <div class="data-card">
            <div class="data-card-header"><h3 class="data-card-title">姣忔棩浜у搧浜ч攢鐜囨槑缁?/h3></div>
            <div class="data-card-body"><p>鏃犱骇鍝佷骇閿€鐜囨槑缁嗘暟鎹€?/p></div>
        </div>
        """

    detail_html = '''
    <div class="data-card">
        <div class="data-card-header">
            <h3 class="data-card-title">姣忔棩浜у搧浜ч攢鐜囨槑缁?/h3>
        </div>
        <div class="data-card-body">
            <p>姣忔棩鍚勪骇鍝佺殑璇︾粏浜ч攢鐜囨暟鎹凡绉昏嚦璇︾粏鏁版嵁椤甸潰銆?/p>
            <p><a href="details.html#daily-ratio-details" class="btn btn-primary">鐐瑰嚮鏌ョ湅姣忔棩鏄庣粏鏁版嵁</a></p>
             <!-- Removed the grid of cards and panel generation -->
        </div> <!-- Close data-card-body -->
    </div> <!-- Close data-card -->
    '''
    return detail_html

def _generate_ratio_content(production_sales_ratio, product_sales_ratio_data, output_dir):
    """鐢熸垚浜ч攢鐜囧垎鏋愰儴鍒嗙殑HTML鍐呭 (绉绘鑷師 _generate_production_sales_ratio_section)

    Args:
        production_sales_ratio (dict): 姣忔棩鎬讳綋浜ч攢鐜囨暟鎹? {date: {'ratio': val, ...}}
        product_sales_ratio_data (list): 姣忔棩浜у搧鏄庣粏鏁版嵁鍒楄〃, [{'date': dt, 'data': df}, ...]
        output_dir (str): 杈撳嚭鐩綍锛岀敤浜庢鏌ュ浘鐗囨枃浠躲€?
    Returns:
        str: 浜ч攢鐜囧垎鏋愰儴鍒嗙殑HTML浠ｇ爜銆?    """
    # Check data validity
    has_summary_data = production_sales_ratio is not None and isinstance(production_sales_ratio, dict) and len(production_sales_ratio) > 0
    has_detail_data = product_sales_ratio_data is not None and isinstance(product_sales_ratio_data, list) and len(product_sales_ratio_data) > 0

    if not has_summary_data and not has_detail_data:
        print("璀﹀憡: 浜ч攢鐜囨眹鎬诲拰鏄庣粏鏁版嵁鍧囦负绌猴紝璺宠繃浜ч攢鐜囬儴鍒嗙敓鎴?)
        return """
        <div class="section">
            <div class="section-header"><h2>浜ч攢鐜囧垎鏋?/h2></div>
            <div class="section-body"><p>鏃犱骇閿€鐜囨暟鎹彲渚涙樉绀恒€?/p></div>
        </div>
        """

    ratio_section_html = '''
    <div class="section">
        <div class="section-header">
            <h2>浜ч攢鐜囧垎鏋?/h2>
        </div>
        <div class="section-body">
    '''

    # Ratio Overview Card
    if has_summary_data:
        try:
            valid_ratios = [data.get('ratio', 0) for data in production_sales_ratio.values() if isinstance(data.get('ratio'), (int, float))]
            if not valid_ratios:
                raise ValueError("鏃犳湁鏁堢殑姣旂巼鏁版嵁")

            avg_ratio = sum(valid_ratios) / len(valid_ratios)
            max_ratio_item = max(production_sales_ratio.items(), key=lambda x: x[1].get('ratio', -1) if isinstance(x[1].get('ratio'), (int, float)) else -1)
            min_ratio_item = min(production_sales_ratio.items(), key=lambda x: x[1].get('ratio', float('inf')) if isinstance(x[1].get('ratio'), (int, float)) else float('inf'))

            max_date = max_ratio_item[0].strftime('%Y-%m-%d') if hasattr(max_ratio_item[0], 'strftime') else str(max_ratio_item[0])
            max_ratio = max_ratio_item[1].get('ratio', 0)
            min_date = min_ratio_item[0].strftime('%Y-%m-%d') if hasattr(min_ratio_item[0], 'strftime') else str(min_ratio_item[0])
            min_ratio = min_ratio_item[1].get('ratio', 0)

            avg_status = "balanced"
            avg_status_text = "骞宠　"
            if avg_ratio < 90:
                avg_status = "surplus"
                avg_status_text = "浜у搧绉帇"
            elif avg_ratio > 110:
                avg_status = "shortage"
                avg_status_text = "搴撳瓨娑堣€?

            ratio_section_html += f'''
            <div class="data-card">
                <div class="data-card-header">
                    <h3 class="data-card-title">浜ч攢鐜囨瑙?/h3>
                </div>
                <div class="data-card-body">
                    <p>浜ч攢鐜囨槸琛￠噺浼佷笟鐢熶骇涓庨攢鍞钩琛℃€х殑閲嶈鎸囨爣锛岃绠楀叕寮忎负锛?strong>浜ч攢鐜?= 閿€閲?/ 浜ч噺 脳 100%</strong>銆?/p>
                    <p style="text-align: right; font-size: 12px; color: #666; margin-top: 5px;">娉細浜ч噺閿€閲忓潎涓嶅寘鍚壇浜у搧鍜岄矞鍝?/p>
                    <div class="inventory-summary"> <!-- Reusing inventory card style -->
                        <div class="inventory-card">
                            <h4><i class="bi bi-speedometer2"></i> 骞冲潎浜ч攢鐜?/h4>
                            <div class="value {avg_status}">{avg_ratio:.0f}%</div>
                            <div class="ratio-date">鏁翠綋鐘舵€? {avg_status_text}</div>
                        </div>
                        <div class="inventory-card">
                            <h4><i class="bi bi-arrow-up-circle"></i> 鏈€楂樹骇閿€鐜?/h4>
                            <div class="value shortage">{max_ratio:.0f}%</div>
                            <div class="ratio-date">鏃ユ湡: {max_date}</div>
                        </div>
                        <div class="inventory-card">
                            <h4><i class="bi bi-arrow-down-circle"></i> 鏈€浣庝骇閿€鐜?/h4>
                            <div class="value surplus">{min_ratio:.0f}%</div>
                            <div class="ratio-date">鏃ユ湡: {min_date}</div>
                        </div>
                    </div>
                </div>
            </div>
            '''
        except Exception as e:
             print(f"鐢熸垚浜ч攢鐜囨瑙堟椂鍑洪敊: {e}")
             ratio_section_html += '<div class="data-card"><div class="data-card-body"><p>鐢熸垚浜ч攢鐜囨瑙堟椂鍑洪敊銆?/p></div></div>'
    else:
         ratio_section_html += '<div class="data-card"><div class="data-card-body"><p>鏃犱骇閿€鐜囨瑙堟暟鎹€?/p></div></div>'

    # Add production sales ratio trend chart
    ratio_chart_filename = "production_sales_ratio.png"
    ratio_chart_path = os.path.join(output_dir, ratio_chart_filename)
    if os.path.exists(ratio_chart_path):
        ratio_section_html += f'''
        <div class="data-card">
            <div class="data-card-header">
                <h3 class="data-card-title">浜ч攢鐜囪秼鍔垮垎鏋?/h3>
            </div>
            <div class="data-card-body">
                <p>涓嬪浘灞曠ず浜嗘瘡鏃ヤ骇閿€鐜囩殑鍙樺寲瓒嬪娍锛屼互鍙婂搴旂殑閿€閲忓拰浜ч噺鏁版嵁銆備骇閿€鐜囨帴杩?00%琛ㄧず鐢熶骇涓庨攢鍞緝涓哄钩琛★紱浣庝簬100%琛ㄧず浜у搧绉帇锛涢珮浜?00%琛ㄧず娑堣€椾簡搴撳瓨銆?/p>
                {generate_image_tag(ratio_chart_filename, alt_text='浜ч攢鐜囪秼鍔垮浘')}
            </div>
        </div>
        '''
    else:
        print(f"浜ч攢鐜囪秼鍔垮浘鏈壘鍒? {ratio_chart_path}")

    # Generate Product Sales Ratio Detail section (now just title and link)
    ratio_section_html += _generate_product_sales_ratio_detail(product_sales_ratio_data)

    ratio_section_html += '''
        </div> <!-- Close section-body -->
    </div> <!-- Close section -->
    '''
    return ratio_section_html

def generate_ratio_page(production_sales_ratio, product_sales_ratio_data, output_dir):
    """鐢熸垚 ratio.html 椤甸潰

    Args:
        production_sales_ratio (dict): 姣忔棩鎬讳綋浜ч攢鐜囨暟鎹€?        product_sales_ratio_data (list): 姣忔棩浜у搧鏄庣粏鏁版嵁鍒楄〃銆?        output_dir (str): HTML 鏂囦欢杈撳嚭鐩綍銆?    """
    print("寮€濮嬬敓鎴?ratio.html 椤甸潰...")
    page_title = "鏄ラ洩椋熷搧鐢熷搧浜ч攢鍒嗘瀽鎶ュ憡 - 浜ч攢鐜囧垎鏋?
    header_html = generate_header(title=page_title, output_dir=output_dir)
    nav_html = generate_navigation(active_page="ratio")
    ratio_content_html = _generate_ratio_content(production_sales_ratio, product_sales_ratio_data, output_dir)
    footer_html = generate_footer()

    full_html = header_html + nav_html + ratio_content_html + footer_html

    write_html_report(full_html, "ratio.html", output_dir)

# # --- Example Usage (for testing) ---
# if __name__ == '__main__':
#     # Create dummy data
#     dummy_ratio_summary = {
#         datetime(2023, 10, 25): {'ratio': 95.5, 'sales': 1000, 'production': 1047},
#         datetime(2023, 10, 26): {'ratio': 105.2, 'sales': 1200, 'production': 1141},
#         datetime(2023, 10, 27): {'ratio': 88.0, 'sales': 900, 'production': 1023}
#     }
#     dummy_product_details = [
#         {
#             'date': datetime(2023, 10, 25),
#             'data': pd.DataFrame({
#                 '鍝佸悕': ['楦¤吙', '楦¤兏', '楦＄繀'],
#                 '閿€閲?: [500, 300, 200],
#                 '浜ч噺': [520, 310, 217],
#                 '浜ч攢鐜?: [96.15, 96.77, 92.16]
#             })
#         },
#         {
#             'date': datetime(2023, 10, 26),
#             'data': pd.DataFrame({
#                 '鍝佸悕': ['楦¤吙', '楦¤兏', '楦＄繀', '楦＄埅'],
#                 '閿€閲?: [600, 350, 220, 30],
#                 '浜ч噺': [580, 330, 200, 31],
#                 '浜ч攢鐜?: [103.45, 106.06, 110.00, 96.77]
#             })
#         },
#         {
#              'date': datetime(2023, 10, 27),
#              'data': pd.DataFrame({
#                  '鍝佸悕': ['楦¤吙', '楦¤兏', '楦＄繀'],
#                  '閿€閲?: [450, 280, 170],
#                  '浜ч噺': [510, 320, 193],
#                  '浜ч攢鐜?: [88.24, 87.50, 88.08]
#              })
#         }
#     ]

#     output_directory = './test_report_output'
#     # Create a dummy image file for testing
#     os.makedirs(output_directory, exist_ok=True)
#     try:
#         with open(os.path.join(output_directory, "production_sales_ratio.png"), 'w') as f:
#             f.write("dummy image content")
#     except OSError as e:
#          print(f"鏃犳硶鍒涘缓娴嬭瘯鍥剧墖: {e}")

#     generate_ratio_page(dummy_ratio_summary, dummy_product_details, output_directory)
#     print(f"娴嬭瘯 ratio.html 宸茬敓鎴愬湪 {output_directory}") 