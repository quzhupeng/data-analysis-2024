# -*- coding: utf-8 -*-
"""
鐢熸垚鎶ュ憡涓婚〉 (index.html)锛屽寘鍚憳瑕佷俊鎭€?
"""

from html_utils import generate_header, generate_navigation, write_html_report
# 瀵煎叆generate_footer浣嗕笉鐩存帴浣跨敤锛屾垜浠皢閲嶅啓杩欎釜鍑芥暟
from html_utils import generate_footer as original_generate_footer

# --- CSS Styles ---
# Moved CSS here to be accessible by generate_index_page
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
        background-color: #fff; /* Keep sections white */
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
    .summary strong {
        color: #0056b3; /* Highlight key metrics */
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
            font-size: 16px; /* Adjust base font size for mobile */
        }
        h2 {
            font-size: 1.5em;
        }
    }
</style>
"""

def _generate_summary_content(summary_data):
    """鐢熸垚鎽樿閮ㄥ垎鐨凥TML鍐呭

    Args:
        summary_data (dict): 鍖呭惈鎽樿鎵€闇€鏁版嵁鐨勫瓧鍏革紝渚嬪:
            {
                'all_data': all_data_df, # For total products/dates
                'abnormal_changes': abnormal_changes_list,
                'inconsistent_records': inconsistent_records_list,
                'missing_dates': missing_dates_list,
                'production_sales_ratio': production_sales_ratio_dict,
                'daily_sales': daily_sales_dict
                # Note: Inventory data is not directly passed here, link will be static
            }
    """
    all_data = summary_data.get('all_data')
    abnormal_changes = summary_data.get('abnormal_changes')
    inconsistent_records = summary_data.get('inconsistent_records') # Used for data consistency check
    missing_dates = summary_data.get('missing_dates') # Used for data integrity check
    production_sales_ratio = summary_data.get('production_sales_ratio')
    daily_sales = summary_data.get('daily_sales')

    # 鏁版嵁姒傝
    total_products = 0
    total_dates = 0
    if all_data is not None and not all_data.empty:
         total_products = all_data['鍝佸悕'].nunique() if '鍝佸悕' in all_data.columns else 0
         total_dates = all_data['鏃ユ湡'].nunique() if '鏃ユ湡' in all_data.columns else 0

    summary_html = f"""
        <div class="section">
            <div class="section-header">
                <h2>鏍稿績鎸囨爣鎽樿</h2>
            </div>
            <div class="section-body">
                <div class="summary">
                    <p><strong>鎶ュ憡鑼冨洿:</strong> 鍒嗘瀽瑕嗙洊 <strong>{total_products}</strong> 绉嶄骇鍝侊紝鏃堕棿璺ㄥ害 <strong>{total_dates}</strong> 澶┿€?/p>
                    <ul>
    """

    # 1. 搴撳瓨鎯呭喌 (Link only, as specific summary data isn't passed)
    summary_html += "<li><strong>搴撳瓨鎯呭喌:</strong> 璇︾粏搴撳瓨姘村钩銆佸懆杞ぉ鏁扮瓑璇峰弬瑙?<a href='inventory.html'>搴撳瓨鍒嗘瀽鎶ュ憡</a>銆?/li>"

    # 2. 浜ч攢鐜囨儏鍐?
    ratio_summary = "" # Default empty string
    if production_sales_ratio and len(production_sales_ratio) > 0:
        try:
            valid_ratios = [data.get('ratio', 0) for data in production_sales_ratio.values() if isinstance(data.get('ratio'), (int, float))]
            if len(valid_ratios) > 0:
                 avg_ratio = sum(valid_ratios) / len(valid_ratios)
                 ratio_summary = f"鏈熼棿骞冲潎浜ч攢鐜囦负 <strong>{avg_ratio:.1f}%</strong>銆?
                 if avg_ratio < 90:
                     ratio_summary += " (鎻愮ず: 鍋忎綆锛屽彲鑳藉瓨鍦ㄧН鍘嬮闄?"
                 elif avg_ratio > 110:
                     ratio_summary += " (鎻愮ず: 鍋忛珮锛屽彲鑳藉瓨鍦ㄧ己璐ч闄?"
                 else:
                     ratio_summary += " (鎻愮ず: 浜ч攢鐩稿骞宠　)"
            else:
                 ratio_summary = "鏃犳硶璁＄畻骞冲潎浜ч攢鐜囷紙鏃犳湁鏁堟暟鎹級銆?
        except Exception as e:
              ratio_summary = f"璁＄畻浜ч攢鐜囨椂鍑洪敊: {e}"
    else:
        ratio_summary = "鏃犱骇閿€鐜囨暟鎹€?
    summary_html += f"<li><strong>浜ч攢鐜囨儏鍐?</strong> {ratio_summary} 璇︾粏鍒嗘瀽璇峰弬瑙?<a href='ratio.html'>浜ч攢鐜囨姤鍛?/a>銆?/li>"


    # 3. 閿€鍞儏鍐?(MODIFIED FOR UNIT CONVERSION)
    sales_summary = "" # Default empty string
    if daily_sales and len(daily_sales) > 0:
        try:
            total_sales_volume_kg = sum(info.get('volume', 0) for info in daily_sales.values() if info and isinstance(info.get('volume'), (int, float)))
            total_sales_volume_tons = total_sales_volume_kg / 1000.0 # Convert KG to Tons

            valid_avg_prices = [info.get('avg_price') for info in daily_sales.values() if info and isinstance(info.get('avg_price'), (int, float))]
            avg_price = sum(valid_avg_prices) / len(valid_avg_prices) if valid_avg_prices else 0
            # Format tons with maybe one decimal place for precision if needed, or keep as int if preferred.
            sales_summary = f"鏈熼棿鎬婚攢閲忕害涓?<strong>{total_sales_volume_tons:,.1f}</strong> 鍚ㄣ€?
            if avg_price > 0:
                 sales_summary += f" 鍔犳潈骞冲潎閿€鍞崟浠风害涓?<strong>{int(avg_price):,}</strong> 鍏?鍚ㄣ€?
        except Exception as e:
              sales_summary = f"璁＄畻閿€鍞憳瑕佹椂鍑洪敊: {e}"
    else:
        sales_summary = "鏃犻攢鍞暟鎹€?
    summary_html += f"<li><strong>閿€鍞儏鍐?</strong> {sales_summary} 璇︾粏瓒嬪娍璇峰弬瑙?<a href='sales.html'>閿€鍞垎鏋愭姤鍛?/a>銆?/li>"

    # 4. 浠锋牸娉㈠姩鎯呭喌 (Focus on large fluctuations)
    price_summary = "" # Default empty string
    if abnormal_changes and len(abnormal_changes) > 0:
        price_summary = "鐩戞祴鍒伴儴鍒嗕骇鍝佷环鏍艰皟鏁磋緝涓洪绻併€? # Changed to a general statement
    else:
        price_summary = "鏈洃娴嬪埌浠锋牸璋冩暣棰戠巼鏄庢樉寮傚父鐨勬儏鍐点€? # Changed to a general statement
    # Link to the page where adjustment records are shown (price_volatility.html)
    summary_html += f"<li><strong>浠锋牸娉㈠姩鎯呭喌:</strong> {price_summary} 璇︾粏璋冧环璁板綍璇峰弬瑙?<a href='price_volatility.html'>浠锋牸娉㈠姩鍒嗘瀽椤?/a>銆?/li>"
    
    # 5. 娣诲姞鍗撳垱璧勮琛屼笟浠锋牸瓒嬪娍瀵艰埅
    summary_html += "<li><strong>琛屼笟浠锋牸瓒嬪娍:</strong> 鏌ョ湅鍗撳垱璧勮鎻愪緵鐨勮涓氫环鏍肩洃娴嬫暟鎹紝璇峰弬瑙?<a href='industry.html'>琛屼笟浠锋牸瓒嬪娍</a>銆?/li>"

    summary_html += "</ul>"

    # Data Integrity/Consistency Notes (Keep them separate)
    integrity_notes = ""
    if missing_dates:
        integrity_notes += f"<p style='font-size:0.9em; color:#666;'>娉細鍙戠幇 {len(missing_dates)} 涓棩鏈熸暟鎹己澶辨垨涓嶅畬鏁淬€?/p>"
    if inconsistent_records and len(inconsistent_records) > 0:
        integrity_notes += f"<p style='font-size:0.9em; color:#666;'>娉細鍙戠幇 <a href='details.html'>{len(inconsistent_records)} 鏉?/a> 璋冨箙涓庝环鏍煎彉鍔ㄤ笉涓€鑷磋褰曘€?/p>"

    if integrity_notes:
        summary_html += "<hr style='border:none; border-top: 1px solid #eee; margin: 15px 0;'>" + integrity_notes

    summary_html += """
                </div>
            </div>
        </div>
    """
    return summary_html

# SECURITY_TAG: PRIVATE_ACCESS_FOOTER_BEGIN
def generate_footer():
    """鐢熸垚HTML椤佃剼锛屽寘鍚殣钘忛摼鎺?""
    from datetime import datetime
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"""
            <div class="section">
                <div class="section-header">
                    <h2>鎶ュ憡璇存槑</h2>
                </div>
                <div class="section-body">
                    <p>鏈姤鍛婃暟鎹潵婧愪簬浼佷笟鍐呴儴绯荤粺銆傛姤鍛婁腑鐨勫垎鏋愮粨鏋滀粎渚涘弬鑰冿紝鍏蜂綋涓氬姟鍐崇瓥璇风粨鍚堝疄闄呮儏鍐点€?/p>
                    <p>濡傛湁浠讳綍闂<a href="private_access.html" style="color:inherit;text-decoration:none;">鎴?/a>寤鸿锛岃鑱旂郴guanlibu@springsnow.cn</p>
                    <p style="text-align: right; margin-top: 20px;">
                        鎶ュ憡鐢熸垚鏃堕棿锛歿current_time}
                    </p>
                </div>
            </div>
        </div> <!-- Close container -->
        <script>
             // Add specific JS calls needed on all pages after DOM load, if any were in the original footer
             // e.g., initializing components
              function searchAbnormal() {{ searchTable('abnormalTable', 'abnormalSearch'); }}
              function searchInconsistent() {{ searchTable('inconsistentTable', 'inconsistentSearch'); }}
              function searchConflict() {{ searchTable('conflictTable', 'conflictSearch'); }}
              function searchComparison() {{ searchTable('comparisonTable', 'comparisonSearch'); }}
              
              // 琛ㄦ牸鎼滅储鍑芥暟 - 鐢ㄤ簬涓€鑸〃鏍兼悳绱?
              function searchTable(tableId, inputId) {{
                  const input = document.getElementById(inputId);
                  const filter = input.value.toUpperCase();
                  const table = document.getElementById(tableId);
                  const tr = table.getElementsByTagName("tr");
                  
                  for (let i = 0; i < tr.length; i++) {{
                      if (i === 0) continue; // 璺宠繃琛ㄥご
                      const td = tr[i].getElementsByTagName("td");
                      let txtValue = "";
                      let visible = false;
                      
                      for (let j = 0; j < td.length; j++) {{
                          if (td[j]) {{
                              txtValue = td[j].textContent || td[j].innerText;
                              if (txtValue.toUpperCase().indexOf(filter) > -1) {{
                                  visible = true;
                                  break;
                              }}
                          }}
                      }}
                      
                      tr[i].style.display = visible ? "" : "none";
                  }}
              }}
              
              // 鍒囨崲闈㈡澘鏄剧ず/闅愯棌
              function togglePanel(panelId, event) {{
                  if (event) event.stopPropagation();
                  const panel = document.getElementById(panelId);
                  if (panel) {{
                      if (panel.style.display === "none" || panel.style.display === "") {{
                          panel.style.display = "block";
                      }} else {{
                          panel.style.display = "none";
                      }}
                  }}
              }}
              
              // 鍒囨崲浜ч攢鐜囨槑缁嗛潰鏉?
              function toggleRatioPanel(dateStr, event) {{
                  if (event) event.stopPropagation();
                  const panelId = `ratioPanel_${{dateStr}}`;
                  togglePanel(panelId, null);
              }}
              
              // 鍒囨崲閿€鍞槑缁嗛潰鏉?
              function toggleSalesPanel(dateStr, event) {{
                  if (event) event.stopPropagation();
                  const panelId = `salesPanel_${{dateStr}}`;
                  togglePanel(panelId, null);
              }}
        </script>
    </body>
</html>
"""
# SECURITY_TAG: PRIVATE_ACCESS_FOOTER_END

def generate_index_page(summary_data, output_dir):
    """鐢熸垚 index.html 椤甸潰

    Args:
        summary_data (dict): 浼犻€掔粰 _generate_summary_content 鐨勬暟鎹瓧鍏搞€?
        output_dir (str): HTML 鏂囦欢杈撳嚭鐩綍銆?
    """
    print("寮€濮嬬敓鎴?index.html 椤甸潰...")
    if not isinstance(summary_data, dict):
        print("閿欒: summary_data 涓嶆槸鏈夋晥鐨勫瓧鍏搞€傛棤娉曠敓鎴?index.html銆?)
        return

    page_title = "鏄ラ洩椋熷搧鐢熷搧浜ч攢鍒嗘瀽鎶ュ憡 - 鎽樿"
    header_html = generate_header(title=page_title)
    nav_html = generate_navigation(active_page="index")
    summary_content_html = _generate_summary_content(summary_data)
    footer_html = generate_footer()

    # --- Add History Link Section Separately ---
    history_section_html = """
    <div class="section">
        <div class="section-header">
            <h2>鍘嗗彶鎶ュ憡瀛樻。</h2>
        </div>
        <div class="section-body">
             <ul>
                 <li><a href='history/'>娴忚杩囧線鏈堜唤鎶ュ憡</a></li>
             </ul>
        </div>
    </div>
    """

    # Construct the full HTML, placing history section after summary, before footer
    full_html = header_html + CSS_STYLES + "<div class='container'>" + nav_html + summary_content_html + history_section_html + "</div>" + footer_html

    write_html_report(full_html, "index.html", output_dir)
    print(f"index.html 椤甸潰宸茬敓鎴愬湪 {output_dir}")

# --- Example Usage (for testing) ---
if __name__ == '__main__':
    import pandas as pd
    # Create dummy data matching the structure expected by _generate_summary_content
    dummy_summary_data = {
        'all_data': pd.DataFrame({'鍝佸悕': ['A', 'B', 'A'], '鏃ユ湡': ['2023-01-01', '2023-01-01', '2023-01-02']}),
        'abnormal_changes': [{'鍝佸悕': 'Product X', '鏃ユ湡': '2023-10-25', '璋冧环娆℃暟': 4}, {'鍝佸悕': 'Product Y', '鏃ユ湡': '2023-10-26', '璋冧环娆℃暟': 3}],
        'inconsistent_records': [{'鍝佸悕': 'Product Z', '鏃ユ湡': '2023-10-25', '璋冨箙': 100, '鍓嶄环鏍?: 5000, '浠锋牸': 4900, '浠锋牸鍙樺姩': -100}],
        'missing_dates': ['2023-10-20', '2023-10-21'],
        'production_sales_ratio': {'2023-10-25': {'ratio': 95.5}, '2023-10-26': {'ratio': 105.2}, '2023-10-27': {'ratio': 'N/A'}}, # Added invalid data for testing
        'daily_sales': {
             '2023-10-25': {'volume': 5000, 'avg_price': 15000, 'product_count': 10, 'data': None, 'quantity_column': '閿€閲?},
             '2023-10-26': {'volume': 6000, 'avg_price': 15500, 'product_count': 12, 'data': None, 'quantity_column': '閿€閲?},
             '2023-10-27': None # Added missing data for testing
        }
    }
    output_directory = './test_report_output'
    generate_index_page(dummy_summary_data, output_directory)
    print(f"娴嬭瘯 index.html 宸茬敓鎴愬湪 {output_directory}")
 