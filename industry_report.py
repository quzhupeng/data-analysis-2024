# -*- coding: utf-8 -*-
"""
鐢熸垚琛屼笟鏁版嵁鎶ュ憡椤甸潰 (industry.html)锛屽睍绀?鍗撳垱璧勮"鐩稿叧鏁版嵁銆?澶勭悊涓変釜Excel鏂囦欢锛?- 鏉垮喕澶ц兏鍘嗗彶浠锋牸.xlsx
- 楦¤嫍鍘嗗彶浠锋牸.xlsx
- 鐞电惗鑵垮巻鍙蹭环鏍?xlsx
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime
from matplotlib.ticker import FuncFormatter
import matplotlib.font_manager as fm
from html_utils import generate_header, generate_navigation, generate_footer, write_html_report, generate_image_tag

# 妫€鏌ュ苟閰嶇疆涓枃瀛椾綋
def setup_chinese_font():
    """妫€鏌ュ苟閰嶇疆涓枃瀛椾綋锛岃繑鍥炲彲鐢ㄧ殑瀛椾綋鍚嶇О"""
    # 妫€鏌ュ父瑙佺殑涓枃瀛椾綋璺緞
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",  # 榛戜綋
        "C:/Windows/Fonts/msyh.ttc",     # 寰蒋闆呴粦
        "C:/Windows/Fonts/msyh.ttf"      # 寰蒋闆呴粦澶囬€夎矾寰?    ]
    
    available_font = None
    
    # 妫€鏌ユ槸鍚︽湁鍙敤鐨勪腑鏂囧瓧浣?    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font_prop = fm.FontProperties(fname=font_path)
                available_font = font_prop
                print(f"宸插姞杞戒腑鏂囧瓧浣? {font_path}")
                break
            except Exception as e:
                print(f"鍔犺浇瀛椾綋 {font_path} 澶辫触: {e}")
    
    if available_font is None:
        print("璀﹀憡: 鏈壘鍒板彲鐢ㄧ殑涓枃瀛椾綋锛屽皢浣跨敤绯荤粺榛樿瀛椾綋")
        available_font = fm.FontProperties(family="sans-serif")
    
    return available_font

# 閰嶇疆鏂囦欢鍜岃矾寰?def generate_industry_charts(industry_data, output_dir):
    """
    鐢熸垚琛屼笟浠锋牸瓒嬪娍鍥?    
    鍙傛暟:
        industry_data (dict): 鍖呭惈鍚勪釜浜у搧浠锋牸鏁版嵁鐨勫瓧鍏?        output_dir (str): 杈撳嚭鐩綍
        
    杩斿洖:
        list: 鐢熸垚鐨勫浘琛ㄦ枃浠惰矾寰勫垪琛?    """
    # 棰勫厛瀹氫箟鍙兘浼氫娇鐢ㄥ埌鐨勫彉閲?    salesTotal = 0  # 閬垮厤寮曠敤閿欒
    productionTotal = 0  # 閬垮厤寮曠敤閿欒
    
    chart_paths = []
    
    # 纭繚杈撳嚭鐩綍瀛樺湪
    os.makedirs(output_dir, exist_ok=True)
    
    # 璁剧疆seaborn鏍峰紡
    sns.set_theme(style="whitegrid")
    
    # 閰嶇疆涓枃瀛椾綋
    chinese_font = setup_chinese_font()
    
    # 瀹氫箟浜у搧鐨勬樉绀洪『搴?    product_order = ['楦¤嫍', '姣涢浮', '鏉垮喕澶ц兏', '鐞电惗鑵?]
    
    # 瀹氫箟涓撲笟閰嶈壊鏂规
    color_palette = {
        '楦¤嫍': '#1976D2',
        '姣涢浮': '#2E7D32',
        '鏉垮喕澶ц兏': '#C62828',
        '鐞电惗鑵?: '#7B1FA2'
    }
    
    # 鎸夌収鎸囧畾椤哄簭鐢熸垚瓒嬪娍鍥?    for product_name in product_order:
        if product_name in industry_data:
            data = industry_data[product_name]
            if data is not None and not data.empty:
                try:
                    # 鍒涘缓鏇村ぇ鐨勫浘琛?                    plt.figure(figsize=(18, 8))
                    ax = plt.gca()
                    
                    # 纭繚鏃ユ湡鍒楁牸寮忔纭?                    if 'date' in data.columns:
                        # 灏濊瘯灏嗘棩鏈熻浆鎹负datetime鏍煎紡
                        data['date'] = pd.to_datetime(data['date'], errors='coerce')
                        
                        # 鎺掑簭鏁版嵁纭繚鏃堕棿绾夸竴鑷存€?                        data = data.sort_values('date')
                        
                        # 璁＄畻浠锋牸鍙樺寲鐜囷紙鐢ㄤ簬鍚庣画鍒嗘瀽锛?                        data['price_pct_change'] = data['price'].pct_change() * 100
                        
                        # 鎵惧嚭鏈€楂樹环鍜屾渶浣庝环
                        max_price_idx = data['price'].idxmax()
                        min_price_idx = data['price'].idxmin()
                        max_price_row = data.loc[max_price_idx]
                        min_price_row = data.loc[min_price_idx]
                        
                        # 璁＄畻鍚堥€傜殑鏁版嵁鐐规娊鏍烽棿闅旓紙閬垮厤鎷ユ尋锛?                        total_points = len(data)
                        sample_interval = max(1, total_points // 30)  # 鏈€澶氭樉绀虹害30涓偣
                        
                        # 缁樺埗浠锋牸瓒嬪娍绾匡紝浣跨敤閫忔槑搴﹀拰鏇寸粏鐨勭嚎鏉?                        ax.plot(data['date'], data['price'], 
                               color=color_palette.get(product_name, '#1976D2'),
                               linewidth=2.5, alpha=0.85)
                        
                        # 娣诲姞绋€鐤忕殑鏁版嵁鐐规爣璁?                        ax.scatter(data['date'][::sample_interval], 
                                  data['price'][::sample_interval],
                                  color=color_palette.get(product_name, '#1976D2'),
                                  s=60, zorder=5, alpha=0.8)
                        
                        # 绐佸嚭鏄剧ず鏈€楂樺拰鏈€浣庝环鏍肩偣
                        ax.scatter(max_price_row['date'], max_price_row['price'], 
                                  color='#D32F2F', s=120, zorder=6, 
                                  edgecolor='white', linewidth=2)
                        ax.scatter(min_price_row['date'], min_price_row['price'], 
                                  color='#388E3C', s=120, zorder=6, 
                                  edgecolor='white', linewidth=2)
                        
                        # 涓烘渶楂樼偣鍜屾渶浣庣偣娣诲姞鏍囩
                        ax.annotate(f"鏈€楂? 楼{max_price_row['price']:.2f}",
                                   xy=(max_price_row['date'], max_price_row['price']),
                                   xytext=(15, 15), textcoords='offset points',
                                   fontsize=14, fontweight='bold', fontproperties=chinese_font,
                                   arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=1.5))
                        
                        ax.annotate(f"鏈€浣? 楼{min_price_row['price']:.2f}",
                                   xy=(min_price_row['date'], min_price_row['price']),
                                   xytext=(15, -25), textcoords='offset points',
                                   fontsize=14, fontweight='bold', fontproperties=chinese_font,
                                   arrowprops=dict(arrowstyle='->', color='#388E3C', lw=1.5))
                        
                        # 璁剧疆鍥捐〃鏍囬鍜岃酱鏍囩
                        plt.title(f'{product_name}鍘嗗彶浠锋牸瓒嬪娍', fontsize=36, fontweight='bold', pad=20, 
                                  fontproperties=chinese_font, color='#222222',
                                  bbox=dict(facecolor='#f9f9f9', edgecolor='#dddddd', boxstyle='round,pad=0.5',
                                           alpha=0.9))
                        plt.xlabel('鏃ユ湡', fontsize=16, labelpad=10, fontproperties=chinese_font)
                        plt.ylabel('浠锋牸 (鍏?kg)', fontsize=16, labelpad=10, fontproperties=chinese_font)
                        
                        # 澧炲ぇ杞村埢搴︽爣绛惧瓧浣?                        ax.tick_params(axis='both', labelsize=14)
                        
                        # 鏍煎紡鍖杫杞翠负璐у竵鏍煎紡
                        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f"楼{x:.2f}"))
                        
                        # 浼樺寲x杞存棩鏈熸牸寮?                        # 涓诲埢搴?- 骞翠唤
                        ax.xaxis.set_major_locator(mdates.YearLocator())
                        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y骞?))
                        
                        # 娆″埢搴?- 姣?涓湀
                        ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
                        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m鏈?))
                        
                        # 寮鸿皟涓诲埢搴︾綉鏍肩嚎
                        ax.grid(which='major', linestyle='-', linewidth=0.7, alpha=0.3)
                        ax.grid(which='minor', linestyle=':', linewidth=0.5, alpha=0.2)
                        
                        # 璁剧疆x杞存爣绛剧殑鏃嬭浆瑙掑害
                        plt.setp(ax.get_xticklabels(which='both'), rotation=45, ha='right', fontproperties=chinese_font)
                        
                        # 濡傛灉鏁版嵁鐐硅秴杩?65涓紙澶х害涓€骞达級锛屾坊鍔?0鏃ョЩ鍔ㄥ钩鍧囩嚎
                        if len(data) > 365:
                            data['MA30'] = data['price'].rolling(window=30).mean()
                            ax.plot(data['date'], data['MA30'], 
                                   color='#FF6F00', linewidth=2, 
                                   linestyle='--', alpha=0.7,
                                   label='30鏃ョЩ鍔ㄥ钩鍧?)
                            plt.legend(loc='upper left', frameon=True, framealpha=0.9,
                                      prop={'size': 14, 'family': chinese_font.get_name()})
                        
                        # 璋冩暣绾佃酱鑼冨洿锛岀暀鍑烘爣娉ㄧ┖闂?                        y_min, y_max = ax.get_ylim()
                        y_range = y_max - y_min
                        ax.set_ylim(y_min - y_range * 0.05, y_max + y_range * 0.1)
                        
                        # 娣诲姞鏁版嵁鏉ユ簮娉ㄩ噴
                        plt.figtext(0.99, 0.01, '鏁版嵁鏉ユ簮: 鍗撳垱璧勮', 
                                    horizontalalignment='right', fontsize=12, 
                                    style='italic', alpha=0.7, fontproperties=chinese_font)
                        
                        # 浣跨敤绱у噾甯冨眬闃叉鍏冪礌婧㈠嚭
                        plt.tight_layout()
                        
                        # 淇濆瓨鍥捐〃锛屽鍔燚PI鎻愰珮娓呮櫚搴?                        chart_filename = f"{product_name}_price_trend.png"
                        chart_path = os.path.join(output_dir, chart_filename)
                        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                        plt.close()
                        
                        print(f"宸茬敓鎴恵product_name}浠锋牸瓒嬪娍鍥? {chart_path}")
                        chart_paths.append(chart_filename)
                    else:
                        print(f"璀﹀憡: {product_name}鏁版嵁缂哄皯鏃ユ湡鍒?)
                except Exception as e:
                    print(f"鐢熸垚{product_name}浠锋牸瓒嬪娍鍥炬椂鍑洪敊: {str(e)}")
            else:
                print(f"璀﹀憡: {product_name}鏁版嵁涓虹┖鎴栨棤鏁?)
    
    return chart_paths

def _generate_industry_content(industry_data, chart_paths, output_dir):
    """鐢熸垚琛屼笟鏁版嵁閮ㄥ垎鐨凥TML鍐呭
    
    Args:
        industry_data (dict): 琛屼笟浠锋牸鏁版嵁瀛楀吀
        chart_paths (list): 鍥捐〃鏂囦欢璺緞鍒楄〃
        output_dir (str): 杈撳嚭鐩綍锛岀敤浜庢鏌ュ浘鐗囨枃浠?        
    Returns:
        str: 琛屼笟鏁版嵁閮ㄥ垎鐨凥TML浠ｇ爜
    """
    # 棰勫厛瀹氫箟鍙兘浼氫娇鐢ㄥ埌鐨勫彉閲?    salesTotal = 0  # 閬垮厤寮曠敤閿欒
    productionTotal = 0  # 閬垮厤寮曠敤閿欒
    
    # 妫€鏌ユ槸鍚︽湁鏈夋晥鏁版嵁
    has_data = industry_data and any(data is not None and not data.empty for data in industry_data.values())
    
    if not has_data:
        return """
        <div class="section">
            <div class="section-header"><h2>琛屼笟浠锋牸瓒嬪娍</h2></div>
            <div class="section-body"><p>鏃犺涓氫环鏍兼暟鎹彲渚涙樉绀恒€?/p></div>
        </div>
        """
    
    html = '''
    <div class="section">
        <div class="section-header">
            <h2>琛屼笟浠锋牸瓒嬪娍</h2>
        </div>
        <div class="section-body">
            <div class="data-card">
                <div class="data-card-header">
                    <h3 class="data-card-title">鍗撳垱璧勮浠锋牸鐩戞祴</h3>
                </div>
                <div class="data-card-body">
                    <p>浠ヤ笅鏄崜鍒涜祫璁洃娴嬬殑涓昏鍐滀骇鍝佷环鏍艰秼鍔匡紝鏁版嵁瀹氭湡鏇存柊銆?/p>
    '''
    
    # 瀹氫箟浜у搧鐨勬樉绀洪『搴?    product_order = ['楦¤嫍', '姣涢浮', '鏉垮喕澶ц兏', '鐞电惗鑵?]
    
    # 鍒涘缓涓€涓浘琛ㄨ矾寰勭殑瀛楀吀锛屾柟渚挎寜椤哄簭鏌ユ壘
    chart_dict = {}
    
    # 鍩轰簬鏂囦欢鍚嶆帹鏂骇鍝佸悕绉帮紝纭繚姝ｇ‘鐨勪骇鍝?鍥捐〃鍖归厤
    for chart_filename in chart_paths:
        # 浠庢枃浠跺悕鎺ㄦ柇浜у搧鍚嶇О锛屼緥濡備粠"姣涢浮_price_trend.png"鎻愬彇"姣涢浮"
        for product_name in product_order:
            if chart_filename.startswith(product_name):
                chart_dict[product_name] = chart_filename
                break
    
    # 鎸夌収鎸囧畾椤哄簭娣诲姞瓒嬪娍鍥?    for product_name in product_order:
        if product_name in industry_data and product_name in chart_dict:
            chart_filename = chart_dict[product_name]
            chart_path = os.path.join(output_dir, chart_filename)
            if os.path.exists(chart_path):
                html += f'''
                <div class="subsection">
                    <h4>{product_name}浠锋牸瓒嬪娍</h4>
                    <div class="chart-container">
                        {generate_image_tag(chart_filename, alt_text=f"{product_name}浠锋牸瓒嬪娍鍥?, css_class="chart")}
                    </div>
                </div>
                '''
            else:
                print(f"璀﹀憡: {product_name}瓒嬪娍鍥炬湭鎵惧埌: {chart_path}")
    
    # 鍒犻櫎鏁版嵁琛ㄦ牸閮ㄥ垎
    
    html += '''
                </div> <!-- Close data-card-body -->
            </div> <!-- Close data-card -->
        </div> <!-- Close section-body -->
    </div> <!-- Close section -->
    '''
    
    return html

def generate_industry_page(industry_data, output_dir):
    """鐢熸垚 industry.html 椤甸潰
    
    Args:
        industry_data (dict): 琛屼笟浠锋牸鏁版嵁瀛楀吀锛屾牸寮忎负 {浜у搧鍚? 鏁版嵁DataFrame}
        output_dir (str): HTML 鏂囦欢杈撳嚭鐩綍
    """
    print(f"{'='*20} 寮€濮嬬敓鎴?industry.html 椤甸潰 {'='*20}")
    print(f"鎺ユ敹鍒扮殑industry_data涓殑閿? {list(industry_data.keys() if industry_data else [])}")
    
    # 閬垮厤寮曠敤鏈畾涔夌殑鍙橀噺
    # 瀹氫箟鍙兘浼氫娇鐢ㄥ埌鐨勫彉閲?    salesTotal = 0  # 棰勫厛瀹氫箟锛岄槻姝㈠紩鐢ㄩ敊璇?    
    # 鐢熸垚鍚勪釜浜у搧鐨勪环鏍艰秼鍔垮浘
    chart_paths = generate_industry_charts(industry_data, output_dir)
    print(f"鐢熸垚鐨刢hart_paths: {chart_paths}")
    
    # 鐢熸垚椤甸潰
    page_title = "鏄ラ洩椋熷搧鐢熷搧浜ч攢鍒嗘瀽鎶ュ憡 - 琛屼笟浠锋牸"
    header_html = generate_header(title=page_title, output_dir=output_dir)
    nav_html = generate_navigation(active_page="industry")
    industry_content_html = _generate_industry_content(industry_data, chart_paths, output_dir)
    footer_html = generate_footer()
    
    full_html = header_html + "<div class='container'>" + nav_html + industry_content_html + "</div>" + footer_html
    
    write_html_report(full_html, "industry.html", output_dir)
    print(f"industry.html 椤甸潰宸茬敓鎴愬湪 {output_dir}")
    
    # 妫€鏌ョ敓鎴愮殑鏂囦欢
    with open(os.path.join(output_dir, "industry.html"), 'r', encoding='utf-8') as f:
        html_content = f.read()
        for product_name in ['楦¤嫍', '姣涢浮', '鏉垮喕澶ц兏', '鐞电惗鑵?]:
            if f'{product_name}浠锋牸瓒嬪娍' in html_content:
                print(f"纭: {product_name}浠锋牸瓒嬪娍宸插寘鍚湪HTML涓?)
            else:
                print(f"璀﹀憡: {product_name}浠锋牸瓒嬪娍鏈寘鍚湪HTML涓?)
    
    print(f"{'='*20} industry.html 椤甸潰鐢熸垚瀹屾垚 {'='*20}")

# 绀轰緥浣跨敤锛堢敤浜庢祴璇曪級
if __name__ == '__main__':
    # 鍒涘缓娴嬭瘯鏁版嵁
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='W')
    
    # 楦¤嫍浠锋牸鏁版嵁
    chicken_data = pd.DataFrame({
        'date': dates,
        'price': [2.5 + i*0.1 + abs(i % 10 - 5)*0.2 for i in range(len(dates))],
        'change': [0.1 if i % 3 == 0 else -0.05 if i % 3 == 1 else 0 for i in range(len(dates))]
    })
    
    # 姣涢浮浠锋牸鏁版嵁
    raw_chicken_data = pd.DataFrame({
        'date': dates,
        'price': [12 + i*0.15 + abs(i % 9 - 4)*0.4 for i in range(len(dates))],
        'change': [0.12 if i % 3 == 0 else -0.08 if i % 3 == 1 else 0 for i in range(len(dates))]
    })
    
    # 鏉垮喕澶ц兏浠锋牸鏁版嵁
    breast_data = pd.DataFrame({
        'date': dates,
        'price': [15 + i*0.2 - abs(i % 8 - 4)*0.5 for i in range(len(dates))],
        'change': [-0.2 if i % 4 == 0 else 0.1 if i % 4 == 1 else 0 for i in range(len(dates))]
    })
    
    # 鐞电惗鑵夸环鏍兼暟鎹?    leg_data = pd.DataFrame({
        'date': dates,
        'price': [18 + i*0.15 + abs(i % 12 - 6)*0.3 for i in range(len(dates))],
        'change': [0.15 if i % 5 == 0 else -0.1 if i % 5 == 1 else 0 for i in range(len(dates))]
    })
    
    # 鍒涘缓琛屼笟鏁版嵁瀛楀吀
    test_industry_data = {
        '楦¤嫍': chicken_data,
        '姣涢浮': raw_chicken_data,
        '鏉垮喕澶ц兏': breast_data,
        '鐞电惗鑵?: leg_data
    }
    
    # 娴嬭瘯鐢熸垚椤甸潰
    output_directory = './test_output'
    os.makedirs(output_directory, exist_ok=True)
    generate_industry_page(test_industry_data, output_directory)
    print(f"娴嬭瘯 industry.html 宸茬敓鎴愬湪 {output_directory}") 