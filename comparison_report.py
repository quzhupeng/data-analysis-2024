# -*- coding: utf-8 -*-
"""
鐢熸垚浠锋牸娉㈠姩鍒嗘瀽鎶ュ憡椤甸潰 (price_volatility.html)銆?鍖呭惈浠锋牸瀵规瘮鍜岃皟浠疯褰曘€?"""

import pandas as pd
from datetime import datetime # Added for get_date helper
from html_utils import generate_header, generate_navigation, generate_footer, write_html_report

# --- CSS Styles (Copied from details_report.py for consistency) ---
CSS_STYLES = """
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f4f4f4;
        color: #333;
        line-height: 1.6;
    }
    .container {
        max-width: 1200px;
        margin: 20px auto;
        padding: 0 20px;
        background-color: #fff;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    nav {
        background-color: #333;
        color: #fff;
        padding: 10px 0;
        text-align: center;
    }
    nav ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    nav ul li {
        display: inline;
        margin: 0 15px;
    }
    nav ul li a {
        color: #fff;
        text-decoration: none;
        font-weight: bold;
        padding: 5px 10px;
        border-radius: 4px;
        transition: background-color 0.3s ease;
    }
    nav ul li a.active,
    nav ul li a:hover {
        background-color: #555;
    }
    .section {
        margin-bottom: 30px;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #fff;
    }
    .section-header {
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .section-header h2 {
        color: #333;
        margin: 0;
    }
    .section-body p, .section-body ul {
        margin-bottom: 15px;
    }
     .section-body ul {
        padding-left: 20px;
    }
    .data-card {
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        overflow: hidden; /* Ensure border-radius clips content */
    }
    .data-card-header {
        background-color: #f8f8f8;
        padding: 10px 15px;
        border-bottom: 1px solid #e0e0e0;
    }
    .data-card-title {
        margin: 0;
        font-size: 1.1em;
        color: #444;
    }
    .data-card-body {
        padding: 15px;
    }
    .detail-search {
        margin-bottom: 15px;
    }
    .detail-search input {
        padding: 8px 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
        width: 100%; /* Full width */
        box-sizing: border-box; /* Include padding in width */
        padding-left: 35px; /* Space for the icon */
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="%23888" viewBox="0 0 16 16"><path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/></svg>'); /* Basic SVG search icon */
        background-repeat: no-repeat;
        background-position: 10px center; /* Position icon inside padding */
    }
    .detail-table-container {
        width: 100%;
        overflow-x: auto; /* Allow horizontal scrolling for wide tables */
        min-height: 400px; /* Ensure it's not too short */
        max-height: 75vh;  /* Limit height to 75% of viewport height */
        overflow-y: auto;  /* Add vertical scroll when exceeding max-height */
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px 12px;
        text-align: left;
        vertical-align: top;
    }
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    tbody tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    tbody tr:hover {
        background-color: #f1f1f1;
    }
    .warning {
        color: #dc3545; /* Red for warnings */
        font-weight: bold;
    }
    .high-value {
        color: #28a745; /* Green for positive changes */
    }
    .low-value {
        color: #dc3545; /* Red for negative changes */
    }
    footer {
        text-align: center;
        margin-top: 30px;
        padding: 15px;
        background-color: #333;
        color: #fff;
        font-size: 0.9em;
    }
    a {
        color: #007bff;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    .text-right {
        text-align: right;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        nav ul li {
            display: block;
            margin: 10px 0;
        }
        .container {
            margin: 10px auto;
            padding: 0 10px;
        }
        .section {
            padding: 15px;
        }
        body {
            font-size: 16px;
        }
        h2 {
            font-size: 1.5em;
        }
        h3.data-card-title {
             font-size: 1.0em;
        }
        th, td {
             padding: 6px 8px;
             font-size: 0.9em;
        }
        .detail-search input {
            padding: 6px 8px;
            padding-left: 30px; /* Adjust padding for mobile */
            background-position: 8px center; /* Adjust icon position */
        }
    }
</style>
"""

# --- Helper function copied from details_report.py ---
def get_date(record):
    date_val = record.get('鏃ユ湡')
    if isinstance(date_val, datetime):
        return date_val
    try:
        return pd.to_datetime(str(date_val)).to_pydatetime()
    except (ValueError, TypeError):
        return datetime.min

# --- Function to generate adjustment table (copied & adapted from details_report.py) ---
def _generate_adjustment_table(conflict_records):
    """鐢熸垚璋冧环璁板綍琛ㄦ牸 (鍐茬獊璁板綍)"""
    print(f"_generate_adjustment_table - 鏀跺埌鐨勮褰曟暟: {len(conflict_records) if conflict_records else 0}")
    adjustment_html = '''
        <div class="data-card">
            <div class="data-card-header">
                <h3 class="data-card-title">璋冧环璁板綍</h3>
            </div>
            <div class="data-card-body">
    '''
    if conflict_records and len(conflict_records) > 0:
        # Sort records by date descending
        try:
            sorted_records = sorted(conflict_records, key=lambda x: datetime.strptime(x.get('鏃ユ湡', '1900-01-01'), '%Y-%m-%d'), reverse=True)
            print(f"璋冧环璁板綍鎺掑簭鍚庣殑璁板綍鏁? {len(sorted_records)}")
        except Exception as e:
            print(f"璋冧环璁板綍鎺掑簭閿欒: {e}")
            sorted_records = conflict_records # Fallback if date format is unexpected

        adjustment_html += '''
                <p>浠ヤ笅涓虹郴缁熻褰曠殑浠锋牸璋冩暣淇℃伅锛堜粎鏄剧ず浠锋牸鏈夊彉鍔ㄧ殑璁板綍锛夛紝鎸夋棩鏈熼檷搴忔帓鍒椼€?/p>
                <p style="text-align: right; font-size: 12px; color: #666; margin-top: 5px;">娉細鏁版嵁鏉ユ簮锛氳皟浠疯〃銆備环鏍煎樊寮?= 浠锋牸 - 鍓嶄环鏍笺€?/p>
                <div class="detail-search">
                    <input type="text" id="conflictSearch" placeholder="杈撳叆鍏抽敭瀛楁悳绱㈣皟浠疯褰?.." onkeyup="searchTable('conflictTable', 'conflictSearch')">
                </div>
                <div class="table-responsive detail-table-container">
                    <table id="conflictTable" class="mobile-friendly-table stacking-table-mobile">
                        <thead>
                            <tr>
                                <th>鏃ユ湡</th>
                                <th>鍝佸悕</th>
                                <th>瑙勬牸</th>
                                <th>鍓嶄环鏍?/th>
                                <th>浠锋牸</th>
                                <th>浠锋牸宸紓</th>
                            </tr>
                        </thead>
                        <tbody>
        '''
        for record in sorted_records:
            date_str = record.get('鏃ユ湡', 'N/A')
            name = record.get('鍝佸悕', 'N/A')
            spec = record.get('瑙勬牸', 'N/A')
            prev_price = record.get('鍓嶄环鏍?, '-')
            curr_price = record.get('浠锋牸', '-')
            diff = record.get('浠锋牸宸紓', '-')

            # Format numbers (Get display versions first)
            try: 
                prev_price_float = float(prev_price) if pd.notna(prev_price) and prev_price != '-' else None
                prev_price_display = f"{prev_price_float:,.0f}" if prev_price_float is not None else '-'
            except: 
                prev_price_display = str(prev_price)
                
            try: 
                curr_price_float = float(curr_price) if pd.notna(curr_price) and curr_price != '-' else None
                curr_price_display = f"{curr_price_float:,.0f}" if curr_price_float is not None else '-'
            except: 
                curr_price_display = str(curr_price)

            # --- Recalculate difference for styling --- START ---
            diff_display = "-" # Default display
            diff_class = ""   # Default class

            # 鐩存帴浣跨敤鍘熷鐨勪环鏍煎樊寮傚€?            try:
                diff_float = float(diff) if pd.notna(diff) and diff != '-' else None
                if diff_float is not None:
                    diff_display = f"{diff_float:,.0f}"
                    
                    # 璁剧疆鏍峰紡鍜岀鍙?                    if diff_float < 0:  # 闄嶄环
                        diff_class = "low-value"  # 绾㈣壊
                    elif diff_float > 0:  # 娑ㄤ环
                        diff_class = "high-value"  # 缁胯壊
                        diff_display = f"+{diff_display}"  # 娣诲姞姝ｅ彿
                else:
                    diff_display = '-'
            except (ValueError, TypeError):
                diff_display = str(diff)  # 鏄剧ず鍘熷鍊?            # --- 缁撴潫浠锋牸宸紓澶勭悊 --- END ---
            
            adjustment_html += f'''
                            <tr>
                                <td data-label="鏃ユ湡">{date_str}</td>
                                <td data-label="鍝佸悕">{name}</td>
                                <td data-label="瑙勬牸">{spec}</td>
                                <td data-label="鍓嶄环鏍? class="text-right">{prev_price_display}</td>
                                <td data-label="浠锋牸" class="text-right">{curr_price_display}</td>
                                <td data-label="浠锋牸宸紓" class="text-right {diff_class}">{diff_display}</td>
                            </tr>
            '''
        adjustment_html += '''
                        </tbody>
                    </table>
                </div> <!-- Close table-responsive -->
            </div>
        '''
    else:
        adjustment_html += "<p>鏃犱环鏍艰皟鏁磋褰曞彲鏄剧ず銆?/p></div>"

    adjustment_html += "</div>" # Close data-card
    return adjustment_html

def _generate_comparison_content(price_comparison_data, conflict_records):
    """鐢熸垚浠锋牸瀵规瘮鍜岃皟浠疯褰曢儴鍒嗙殑HTML鍐呭"

    Args:
        price_comparison_data (pd.DataFrame): 浠锋牸瀵规瘮鏁版嵁銆?        conflict_records (list): 璋冧环璁板綍鍒楄〃銆?
    Returns:
        str: 鍖呭惈涓や釜閮ㄥ垎鐨凥TML浠ｇ爜銆?        """
    print(f"_generate_comparison_content - 鏀跺埌鐨勫啿绐佽褰曟暟: {len(conflict_records) if conflict_records else 0}")

    comparison_section = '''
    <div class="section">
        <div class="section-header">
             <h2>浠锋牸娉㈠姩鍒嗘瀽</h2> <!-- Changed Title -->
        </div>
        <div class="section-body">
    '''

    # --- Price Comparison Table ---
    if price_comparison_data is None or price_comparison_data.empty:
        comparison_section += """
             <div class="data-card">
                 <div class="data-card-header"><h3 class="data-card-title">鏄ラ洩涓庡皬鏄庡啘鐗т环鏍煎姣?/h3></div>
                 <div class="data-card-body"><p>鏃犱环鏍煎姣旀暟鎹彲渚涙樉绀恒€?/p></div>
             </div>
        """
    else:
        comparison_section += '''
             <div class="data-card">
                 <div class="data-card-header">
                     <h3 class="data-card-title">鏄ラ洩涓庡皬鏄庡啘鐗т环鏍煎姣?/h3>
                 </div>
                 <div class="data-card-body">
                    <p>浠ヤ笅鏄槬闆鍝佷笌灏忔槑鍐滅墽鐨勪环鏍煎姣旀暟鎹紝涓棿浠峰樊涓鸿礋鏁拌〃绀烘槬闆环鏍间綆浜庡皬鏄庡啘鐗с€?/p>
                    <p style="text-align: right; font-size: 12px; color: #666; margin-top: 5px;">娉細鏄ラ洩浠锋牸涓鸿皟浠疯〃鏈€鏂颁环鏍硷紝灏忔槑鍐滅墽鍙栦腑闂翠环</p>
                    <div class="detail-search">
                        <input type="text" id="comparisonSearch" placeholder="杈撳叆鍏抽敭瀛楁悳绱㈠姣?.." onkeyup="searchTable('comparisonTable', 'comparisonSearch')"> <!-- Adjusted JS call -->
                    </div>
                    <div class="table-responsive detail-table-container">
                        <table id="comparisonTable" class="mobile-friendly-table stacking-table-mobile">
                            <thead>
                                <tr>
                                    <th>鍝佸悕</th>
                                    <th>瑙勬牸</th>
                                    <th>鏄ラ洩浠锋牸</th>
                                    <th>灏忔槑涓棿浠?/th>
                                    <th>涓棿浠峰樊</th>
                                </tr>
                            </thead>
                            <tbody>
    '''
    required_cols = ['鍝佸悕', '瑙勬牸', '鏄ラ洩浠锋牸', '灏忔槑涓棿浠?, '涓棿浠峰樊']
    if not all(col in price_comparison_data.columns for col in required_cols):
        comparison_section += "<tr><td colspan='5'>浠锋牸瀵规瘮鏁版嵁鍒椾笉瀹屾暣銆?/td></tr>"
    else:
        sorted_data = price_comparison_data
        for _, row in sorted_data.iterrows():
            prod_name = row.get('鍝佸悕', 'N/A')
            spec = row.get('瑙勬牸', '')
            spring_price_val = row.get('鏄ラ洩浠锋牸')
            xiaoming_price_val = row.get('灏忔槑涓棿浠?)
            price_diff_val = row.get('涓棿浠峰樊')
            spring_price_display = "-"
            if pd.notna(spring_price_val):
                try: spring_price_display = f"{float(spring_price_val):,.0f}"
                except (ValueError, TypeError): spring_price_display = str(spring_price_val)
            xiaoming_price_display = "-"
            if pd.notna(xiaoming_price_val):
                 try: xiaoming_price_display = f"{float(xiaoming_price_val):,.0f}"
                 except (ValueError, TypeError): xiaoming_price_display = str(xiaoming_price_val)
            price_diff_display = "-"
            price_diff_class = ""
            if pd.notna(price_diff_val):
                try:
                    price_diff_float = float(price_diff_val)
                    price_diff_display = f"{price_diff_float:,.0f}"
                    if price_diff_float < 0:
                        price_diff_class = "warning" # Negative difference highlighted
                except (ValueError, TypeError):
                    price_diff_display = str(price_diff_val)
            comparison_section += f'''
                <tr>
                    <td data-label="鍝佸悕">{prod_name}</td>
                    <td data-label="瑙勬牸">{spec}</td>
                    <td data-label="鏄ラ洩浠锋牸" class="text-right">{spring_price_display}</td>
                    <td data-label="灏忔槑涓棿浠? class="text-right">{xiaoming_price_display}</td>
                    <td data-label="涓棿浠峰樊" class="text-right {price_diff_class}">{price_diff_display}</td>
                </tr>
            '''
    comparison_section += '''
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        '''

    # --- Adjustment Table (Moved from details) ---
    comparison_section += _generate_adjustment_table(conflict_records)

    comparison_section += '''
        </div> <!-- Close section-body -->
    </div> <!-- Close section -->
    '''
    return comparison_section

def generate_comparison_page(price_comparison_data, conflict_records, output_dir):
    """鐢熸垚 price_volatility.html 椤甸潰 (鍘?comparison.html)

    Args:
        price_comparison_data (pd.DataFrame): 浠锋牸瀵规瘮鏁版嵁銆?        conflict_records (list): 璋冧环璁板綍鍒楄〃銆?        output_dir (str): HTML 鏂囦欢杈撳嚭鐩綍銆?    """
    print("寮€濮嬬敓鎴?price_volatility.html 椤甸潰...")
    print(f"generate_comparison_page - 鏀跺埌鐨勫啿绐佽褰曟暟: {len(conflict_records) if conflict_records else 0}")
    page_title = "鏄ラ洩椋熷搧鐢熷搧浜ч攢鍒嗘瀽鎶ュ憡 - 浠锋牸娉㈠姩鍒嗘瀽" # Changed Title
    header_html = generate_header(title=page_title, output_dir=output_dir)
    # Changed active_page identifier
    nav_html = generate_navigation(active_page="price_volatility")
    comparison_content_html = _generate_comparison_content(price_comparison_data, conflict_records)
    footer_html = generate_footer()

    # Add CSS Styles to the beginning of the body or within the head if possible
    # Assuming header_html contains <head>...</head><body>, inject CSS after </head>
    # Or better, modify generate_header if possible. For now, inject after header.
    full_html = header_html + CSS_STYLES + "<div class='container'>" + nav_html + comparison_content_html + "</div>" + footer_html

    # Changed output filename
    write_html_report(full_html, "price_volatility.html", output_dir)
    print(f"price_volatility.html generated in {output_dir}")

# --- Example Usage (Updated for testing) ---
if __name__ == '__main__':
    # Create dummy comparison data
    dummy_comp_data = pd.DataFrame({
        '鍝佸悕': ['楦″ぇ鑳?, '楦＄繀涓?, '鐞电惗鑵?, '楦＄埅'],
        '瑙勬牸': ['A', 'B', 'C', 'D'],
        '鏄ラ洩浠锋牸': [10000, 15000, 9000, 12000],
        '灏忔槑涓棿浠?: [10200, 14800, 9500, 12000],
        '涓棿浠峰樊': [-200, 200, -500, 0]
    })
    dummy_comp_data.loc[4] = ['楦″績', 'E', 8000, None, None]

    # Create dummy conflict (adjustment) data
    dummy_conflict = [
        {'鏃ユ湡': '2023-10-27', '鍝佸悕': 'Product F', '瑙勬牸': 'Spec2', '鍓嶄环鏍?: 7000, '浠锋牸': 7250},
        {'鏃ユ湡': '2023-10-27', '鍝佸悕': 'Product F', '瑙勬牸': 'Spec2', '鍓嶄环鏍?: 7250, '浠锋牸': 7100},
        {'鏃ユ湡': '2023-10-26', '鍝佸悕': 'Product G', '瑙勬牸': 'Spec1', '鍓嶄环鏍?: 8000, '浠锋牸': 8000}, # Zero diff
        {'鏃ユ湡': '2023-10-28', '鍝佸悕': 'Product H', '瑙勬牸': None, '鍓嶄环鏍?: 9000, '浠锋牸': 8800},
    ]

    output_directory = './test_report_output'
    import os
    os.makedirs(output_directory, exist_ok=True)

    # Call the updated function with both datasets
    generate_comparison_page(dummy_comp_data, dummy_conflict, output_directory)
    print(f"娴嬭瘯 price_volatility.html 宸茬敓鎴愬湪 {output_directory}") 