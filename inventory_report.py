# -*- coding: utf-8 -*-
"""
鐢熸垚搴撳瓨鎯呭喌鎶ュ憡椤甸潰 (inventory.html)銆?"""

import os
import pandas as pd
# --- 淇瀵煎叆 ---
# 浠?html_utils 瀵煎叆鍩虹 HTML 鐢熸垚鍑芥暟
from html_utils import (
    generate_header,
    generate_navigation,
    generate_footer,
    write_html_report,
    generate_image_tag
    # 绉婚櫎浜?format_dataframe, format_currency, format_number
)
# 浠?utils.report_utils 瀵煎叆鏍煎紡鍖栧嚱鏁?(鍋囪瀹冧滑鍦ㄨ繖閲?
try:
    from utils.report_utils import format_number # 鍙鍏ュ疄闄呯敤鍒扮殑
    # 濡傛灉杩橀渶瑕?format_dataframe 鎴?format_currency锛屼篃鍦ㄨ繖閲屽鍏?    # from utils.report_utils import format_dataframe, format_currency
except ModuleNotFoundError:
    print("閿欒锛氭棤娉曚粠 'utils.report_utils' 瀵煎叆鏍煎紡鍖栧嚱鏁般€傝纭繚 'utils' 鐩綍瀛樺湪锛屽寘鍚?'__init__.py' 鍜?'report_utils.py' 鏂囦欢锛屼笖鍚庤€呭畾涔変簡鎵€闇€鍑芥暟銆?)
    # 鎻愪緵涓€涓复鏃剁殑銆佸熀鏈殑 format_number 鍑芥暟浠ラ伩鍏嶅畬鍏ㄥ穿婧?    def format_number(value, precision=0):
        if pd.isna(value):
            return "-"
        try:
            return f"{float(value):,.{precision}f}"
        except (ValueError, TypeError):
            return str(value)
# ----------------

def _generate_inventory_content(inventory_data, output_dir):
    """鐢熸垚搴撳瓨鎯呭喌閮ㄥ垎鐨凥TML鍐呭 (绉绘鑷師 _generate_inventory_section)

    Args:
        inventory_data (pd.DataFrame): 搴撳瓨鏁版嵁銆?        output_dir (str): 杈撳嚭鐩綍锛岀敤浜庢鏌ュ浘鐗囨枃浠躲€?
    Returns:
        str: 搴撳瓨閮ㄥ垎鐨凥TML浠ｇ爜銆?    """
    # Handle cases where inventory_data might be None or empty
    if inventory_data is None or inventory_data.empty:
        return """
        <div class="section">
            <div class="section-header"><h2>搴撳瓨鎯呭喌</h2></div>
            <div class="section-body"><p>鏃犲簱瀛樻暟鎹彲渚涙樉绀恒€?/p></div>
        </div>
        """

    # Inventory summary cards
    total_inventory_kg = inventory_data['搴撳瓨閲?].sum() if '搴撳瓨閲? in inventory_data.columns else 0
    total_production_kg = inventory_data['浜ч噺'].sum() if '浜ч噺' in inventory_data.columns else 0
    total_sales_kg = inventory_data['閿€閲?].sum() if '閿€閲? in inventory_data.columns else 0

    # Convert to Tons
    total_inventory_tons = total_inventory_kg / 1000.0
    total_production_tons = total_production_kg / 1000.0
    total_sales_tons = total_sales_kg / 1000.0

    inventory_section = f"""
    <div class="section">
        <div class="section-header">
            <h2>搴撳瓨鎯呭喌</h2>
        </div>
        <div class="section-body">
            <div class="inventory-summary">
                <div class="inventory-card">
                    <h4><i class="bi bi-box-seam"></i> 鎬诲簱瀛橀噺 (鍚?</h4>
                    <div class="value">{format_number(total_inventory_tons, precision=1)}</div>
                </div>
                <div class="inventory-card">
                    <h4><i class="bi bi-gear"></i> 鎬讳骇閲?(鍏ュ簱, 鍚?</h4>
                    <div class="value">{format_number(total_production_tons, precision=1)}</div>
                </div>
                <div class="inventory-card">
                    <h4><i class="bi bi-cart"></i> 鎬婚攢閲?(鍑哄簱, 鍚?</h4>
                    <div class="value">{format_number(total_sales_tons, precision=1)}</div>
                </div>
            </div>
            <p style="text-align: right; font-size: 12px; color: #666; margin-top: 5px;">娉細搴撳瓨鍙ｅ緞涓哄幓闄ら矞鍝併€佸壇浜у搧鍚庛€備骇閲忎负鍏ュ簱閲忥紝閿€閲忎负鍑哄簱閲忋€傚崱鐗囨暟鍊煎崟浣嶄负鍚ㄣ€?/p>
    """

    # Inventory visualization chart
    inventory_chart_filename = "inventory_top_items.png"
    inventory_chart_path = os.path.join(output_dir, inventory_chart_filename)
    if os.path.exists(inventory_chart_path):
        print(f"DEBUG: Inventory chart found: {inventory_chart_path}") # 淇濈暀璋冭瘯淇℃伅
        inventory_section += f"""
            <div class="data-card">
                <div class="data-card-header">
                    <h3 class="data-card-title">搴撳瓨鍙鍖?/h3>
                </div>
                <div class="data-card-body">
                    <div>
                        <h4>搴撳瓨閲廡OP15浜у搧</h4>
                        {generate_image_tag(inventory_chart_filename, alt_text="搴撳瓨閲廡OP15浜у搧", css_class="img-fluid")}
                    </div>
                </div>
            </div>
        """
    else:
        print(f"WARNING: Inventory chart NOT found at: {inventory_chart_path}") # 淇濈暀璀﹀憡淇℃伅
        # 鍙互閫夋嫨鎬у湴娣诲姞鍗犱綅绗︽垨鎻愮ず
        inventory_section += """
            <div class="data-card">
                <div class="data-card-header"><h3 class="data-card-title">搴撳瓨鍙鍖?/h3></div>
                <div class="data-card-body"><p>搴撳瓨閲廡OP15浜у搧鍥捐〃鏈敓鎴愭垨鏈壘鍒般€?/p></div>
            </div>
        """

    # Inventory detail table
    inventory_section += """
        <div class="data-card">
            <div class="data-card-header">
                <h3 class="data-card-title">搴撳瓨鏄庣粏琛?/h3>
            </div>
            <div class="data-card-body">
                <div class="inventory-search">
                    <input type="text" id="inventorySearch" placeholder="杈撳叆鍏抽敭瀛楁悳绱㈠簱瀛?.." onkeyup="searchTable('inventoryTable', 'inventorySearch')">
                </div>
                <div class="inventory-table-container detail-table-container">
                    <table id="inventoryTable">
                        <thead>
                            <tr>
                                <th>鍝佸悕</th>
                                <th class="text-right">浜ч噺</th>
                                <th class="text-right">閿€閲?/th>
                                <th class="text-right">搴撳瓨閲?/th>
                            </tr>
                        </thead>
                        <tbody>
    """

    # Add data rows - sort by inventory quantity descending
    display_columns = ['鍝佸悕', '浜ч噺', '閿€閲?, '搴撳瓨閲?]
    if all(col in inventory_data.columns for col in display_columns):
        # 纭繚鍦ㄦ帓搴忓墠澶勭悊 NaN 鍊硷紝鍚﹀垯鍙兘瀵艰嚧閿欒
        sorted_inventory = inventory_data[display_columns].fillna({'搴撳瓨閲?: -float('inf')}).sort_values(by='搴撳瓨閲?, ascending=False).replace({-float('inf'): pd.NA})

        for _, row in sorted_inventory.iterrows():
            inventory_section += "<tr>"
            # 鍝佸悕鍒?            inventory_section += f"<td>{row.get('鍝佸悕', 'N/A')}</td>"
            # 鏁板€煎垪鏍煎紡鍖?            for col in ['浜ч噺', '閿€閲?, '搴撳瓨閲?]:
                value = row.get(col)
                # 浣跨敤 format_number 澶勭悊 NaN 鍜屾暟瀛?                value_display = format_number(value, precision=0) # 鍋囪 format_number 鑳藉鐞?NaN/None
                inventory_section += f"<td class=\"text-right\">{value_display}</td>"
            inventory_section += "</tr>"
    else:
        missing_cols = [col for col in display_columns if col not in inventory_data.columns]
        inventory_section += f"<tr><td colspan='4'>搴撳瓨鏄庣粏鍒椾笉瀹屾暣 (缂哄皯: {', '.join(missing_cols)}) 鎴栨暟鎹牸寮忛敊璇€?/td></tr>"

    inventory_section += """
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div> <!-- Close section-body -->
</div> <!-- Close section -->
    """

    return inventory_section

def generate_inventory_page(inventory_data, output_dir):
    """鐢熸垚 inventory.html 椤甸潰

    Args:
        inventory_data (pd.DataFrame): 搴撳瓨鏁版嵁銆?        output_dir (str): HTML 鏂囦欢杈撳嚭鐩綍銆?    """
    print("寮€濮嬬敓鎴?inventory.html 椤甸潰...")
    page_title = "鏄ラ洩椋熷搧鐢熷搧浜ч攢鍒嗘瀽鎶ュ憡 - 搴撳瓨鎯呭喌"
    header_html = generate_header(title=page_title, output_dir=output_dir)
    nav_html = generate_navigation(active_page="inventory")
    inventory_content_html = _generate_inventory_content(inventory_data, output_dir)
    footer_html = generate_footer()

    full_html = header_html + "<div class='container'>" + nav_html + inventory_content_html + "</div>" + footer_html

    write_html_report(full_html, "inventory.html", output_dir)

# # --- Example Usage (for testing) ---
# if __name__ == '__main__':
#     # Create dummy inventory data
#     dummy_data = {
#         '鍝佸悕': [f'Product {i}' for i in range(20)],
#         '浜ч噺': [1000 + i * 50 for i in range(20)],
#         '閿€閲?: [800 + i * 40 for i in range(20)],
#         '搴撳瓨閲?: [2000 - i * 100 for i in range(20)]
#     }
#     dummy_inventory_df = pd.DataFrame(dummy_data)
#     dummy_inventory_df.loc[3, '搴撳瓨閲?] = None # Add a NaN value for testing

#     output_directory = './test_report_output'
#     # Create a dummy image file for testing
#     os.makedirs(output_directory, exist_ok=True)
#     try:
#         with open(os.path.join(output_directory, "top15_inventory_qty.png"), 'w') as f:
#             f.write("dummy image content")
#     except OSError as e:
#         print(f"鏃犳硶鍒涘缓娴嬭瘯鍥剧墖: {e}")

#     generate_inventory_page(dummy_inventory_df, output_directory)
#     print(f"娴嬭瘯 inventory.html 宸茬敓鎴愬湪 {output_directory}") 