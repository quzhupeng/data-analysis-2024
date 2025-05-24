# -*- coding: utf-8 -*-
"""
鍙鍖栨ā鍧楋紝璐熻矗鐢熸垚鍚勭鍥捐〃
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import pandas as pd
import seaborn as sns
from datetime import datetime
import matplotlib
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.font_manager import FontProperties
import matplotlib.ticker as mticker

# 璁剧疆涓枃鏄剧ず
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 鐢ㄦ潵姝ｅ父鏄剧ず涓枃鏍囩
matplotlib.rcParams['axes.unicode_minus'] = False  # 鐢ㄦ潵姝ｅ父鏄剧ず璐熷彿
matplotlib.rcParams['xtick.labelsize'] = 12  # 澧炲ぇx杞存爣绛惧瓧浣撳ぇ灏?matplotlib.rcParams['ytick.labelsize'] = 12  # 澧炲ぇy杞存爣绛惧瓧浣撳ぇ灏?matplotlib.rcParams['axes.titlesize'] = 14  # 澧炲ぇ鏍囬瀛椾綋澶у皬
matplotlib.rcParams['axes.labelsize'] = 12  # 澧炲ぇ杞存爣绛惧瓧浣撳ぇ灏?
import config


class DataVisualizer:
    """鏁版嵁鍙鍖栫被锛岃礋璐ｇ敓鎴愬悇绉嶅浘琛?""
    
    def __init__(self, output_dir=None):
        """
        鍒濆鍖栧彲瑙嗗寲鍣?        
        鍙傛暟:
            output_dir: 杈撳嚭鐩綍
        """
        self.output_dir = output_dir or config.OUTPUT_DIR
        # 纭繚杈撳嚭鐩綍瀛樺湪
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_abnormal_timeline(self, abnormal_changes):
        """
        鐢熸垚寮傚父娉㈠姩鏃堕棿杞村浘
        
        鍙傛暟:
            abnormal_changes: 寮傚父娉㈠姩璁板綍
        
        杩斿洖:
            chart_path: 鐢熸垚鐨勫浘琛ㄦ枃浠惰矾寰?        """
        if not abnormal_changes:
            print("娌℃湁寮傚父娉㈠姩鏁版嵁锛屾棤娉曠敓鎴愭椂闂磋酱鍥?)
            return None
        
        try:
            # 杞崲涓篋ataFrame
            abnormal_df = pd.DataFrame(abnormal_changes)
            abnormal_counts = abnormal_df.groupby('鏃ユ湡').size()
            
            plt.figure(figsize=(12, 6))
            sns.lineplot(x=abnormal_counts.index, y=abnormal_counts.values, marker='o', linewidth=2)
            plt.title('寮傚父娉㈠姩鏃堕棿杞?)
            plt.xlabel('鏃ユ湡')
            plt.ylabel('寮傚父娉㈠姩浜у搧鏁伴噺')
            plt.grid(True)
            plt.tight_layout()
            
            # 淇濆瓨鍥捐〃
            chart_path = os.path.join(self.output_dir, 'abnormal_timeline.png')
            plt.savefig(chart_path, dpi=300)
            plt.close()
            
            print(f"寮傚父娉㈠姩鏃堕棿杞村浘宸蹭繚瀛樿嚦: {chart_path}")
            return chart_path
        
        except Exception as e:
            print(f"鐢熸垚寮傚父娉㈠姩鏃堕棿杞村浘鍑洪敊: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_inventory_visualization(self, inventory_data):
        """
        鐢熸垚搴撳瓨鍙鍖栧浘琛?        
        鍙傛暟:
            inventory_data: 搴撳瓨鏁版嵁
        
        杩斿洖:
            chart_path: 鐢熸垚鐨勫浘琛ㄦ枃浠惰矾寰?        """
        if inventory_data is None or inventory_data.empty:
            print("娌℃湁搴撳瓨鏁版嵁鍙緵鍙鍖?)
            return None
        
        try:
            plt.figure(figsize=(12, 7))
            # Assuming '搴撳瓨閲? is the column to plot
            # Let's plot top N items by inventory
            top_n = 15
            plot_data = inventory_data.nlargest(top_n, '搴撳瓨閲?)

            bars = plt.bar(plot_data['鍝佸悕'], plot_data['搴撳瓨閲?], color='skyblue') # Store the bars
            plt.xlabel('浜у搧鍚嶇О')
            plt.ylabel('搴撳瓨閲?)
            plt.title(f'搴撳瓨閲忔渶楂樼殑 {top_n} 绉嶄骇鍝?)
            plt.xticks(rotation=45, ha='right')

            # --- Add value labels on top of bars --- 
            for bar in bars:
                height = bar.get_height()
                if height > 0: # Only label bars with positive height
                    plt.annotate(f'{height:,.0f}', # Format as integer with comma
                                 xy=(bar.get_x() + bar.get_width() / 2, height),
                                 xytext=(0, 3),  # 3 points vertical offset
                                 textcoords="offset points",
                                 ha='center', va='bottom',
                                 fontsize=9) # Adjust font size if needed
            # --- End value labels ---

            plt.tight_layout()

            chart_path = os.path.join(self.output_dir, 'inventory_top_items.png')
            plt.savefig(chart_path, dpi=150)
            plt.close()
            print(f"Inventory visualization saved to {chart_path}")
            return chart_path
        except Exception as e:
            print(f"Error generating inventory visualization: {e}")
            return None
    
    def generate_daily_sales_trend(self, daily_sales):
        """
        鐢熸垚姣忔棩閿€鍞儏鍐垫姌绾垮浘
        
        鍙傛暟:
            daily_sales: 姣忔棩閿€鍞暟鎹?        
        杩斿洖:
            chart_path: 鐢熸垚鐨勫浘琛ㄦ枃浠惰矾寰?        """
        if not daily_sales or len(daily_sales) == 0:
            print("娌℃湁閿€鍞暟鎹紝鏃犳硶鐢熸垚閿€鍞秼鍔垮浘")
            return None
        
        try:
            # Prepare data for plotting
            dates = sorted(daily_sales.keys())
            volumes = [daily_sales[d].get('volume', 0) for d in dates]
            avg_prices = [daily_sales[d].get('avg_price') for d in dates]
            # Convert price Nones to NaN for plotting, handle non-numeric gracefully
            numeric_prices = []
            for p in avg_prices:
                try:
                    numeric_prices.append(float(p) if p is not None else None)
                except (ValueError, TypeError):
                    numeric_prices.append(None) # Treat unconvertible values as None
            avg_prices = numeric_prices

            # Create figure and axes
            fig, ax1 = plt.subplots(figsize=(15, 8)) # Keep standard size

            # Plot daily sales volume (left y-axis)
            color = 'tab:blue'
            ax1.set_xlabel('鏃ユ湡')
            ax1.set_ylabel('鏃ラ攢閲?(鍏枻/鍗曚綅)', color=color)
            ax1.plot(dates, volumes, color=color, marker='o', linestyle='-', label='鏃ラ攢閲?)
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.tick_params(axis='x', rotation=45)
            ax1.grid(True, axis='y', linestyle='--', alpha=0.7)
            # Format Y-axis with commas
            ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: format(int(x), ',')))

            # Create a second y-axis for average price (right y-axis)
            ax2 = ax1.twinx()
            color = 'tab:red'
            ax2.set_ylabel('鏃ュ潎鍚◣鍗曚环 (鍏?鍚?', color=color)
            ax2.plot(dates, avg_prices, color=color, marker='x', linestyle='--', label='鏃ュ潎浠?)
            ax2.tick_params(axis='y', labelcolor=color)
             # Format Y-axis with commas
            ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: format(int(x), ',')))

            # Add annotations (labels on points) - Modified for mobile
            for i, (volume, price) in enumerate(zip(volumes, avg_prices)):
                 # Sales volume annotation (less dense)
                 if (i % 2 == 0 or i == len(volumes)-1) and pd.notna(volume):
                    ax1.annotate(f'{volume:,.0f}',
                                   xy=(dates[i], volume),
                                   xytext=(0, 10), # Offset slightly above
                                   textcoords='offset points',
                                   ha='center', va='bottom',
                                   color='tab:blue',
                                   fontsize=9)

                 # Average price annotation (less dense)
                 if (i % 2 == 1 or i == len(avg_prices)-1) and pd.notna(price):
                    ax2.annotate(f'{price:,.0f}',
                                   xy=(dates[i], price),
                                   xytext=(0, -15), # Offset slightly below
                                   textcoords='offset points',
                                   ha='center', va='top',
                                   color='tab:red',
                                   fontsize=9)

            # Add title and legend
            plt.title('姣忔棩閿€鍞噺涓庡钩鍧囧崟浠疯秼鍔?, fontsize=16)
            # Combine legends from both axes
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

            # Improve layout
            plt.tight_layout(pad=1.2) # Keep padding

            # Save the chart
            chart_path = os.path.join(self.output_dir, 'daily_sales_trend.png')
            plt.savefig(chart_path, dpi=300, bbox_inches='tight') # Keep high DPI
            plt.close()
            print(f"Daily sales trend chart saved to {chart_path}")
            return chart_path
        except Exception as e:
            print(f"Error generating daily sales trend chart: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_production_sales_ratio_visualization(self, production_sales_ratio, output_file="production_sales_ratio.png"):
        """鐢熸垚浜ч攢鐜囪秼鍔垮浘"""
        # 杩欓噷鐨勯€昏緫涓嶉渶瑕佷慨鏀癸紝鍥犱负瀹冧娇鐢ㄧ殑鏄凡缁忚绠楀ソ鐨勪骇閿€鐜囨暟鎹?        # 浣嗗彲浠ユ洿鏂板浘琛ㄦ爣棰樻垨璇存槑锛屾槑纭暟鎹潵婧?        
        plt.figure(figsize=(12, 6))
        # ... 缁樺浘浠ｇ爜 ...
        plt.title("浜ч攢鐜囪秼鍔?(鏁版嵁鏉ユ簮: 浜ф垚鍝佸叆搴撳垪琛?& 閿€鍞彂绁ㄦ墽琛屾煡璇?", fontsize=14)
        # ... 鍏朵粬缁樺浘浠ｇ爜 ...
    
    def generate_production_sales_ratio_chart(self, ratio_summary, chart_path):
        """Generates production vs. sales ratio line chart with filled areas."""
        if not ratio_summary:
            print("No ratio summary data to visualize.")
            return None

        try:
            dates = sorted(ratio_summary.keys())
            ratios = np.array([ratio_summary[d].get('ratio', 0) for d in dates])

            plt.figure(figsize=(15, 8))
            ax = plt.gca()

            # Plot the main ratio line
            line, = ax.plot(dates, ratios, marker='o', linestyle='-', color='purple', linewidth=2, markersize=6, label='缁煎悎浜ч攢鐜?)

            # --- Add fill_between logic back --- 
            baseline = 100
            # Fill green where ratio > 100 (Consuming inventory)
            ax.fill_between(dates, ratios, baseline,
                              where=ratios >= baseline,
                              interpolate=True,
                              color='lightgreen', alpha=0.4, label='娑堣€楀簱瀛樺尯 (>100%)')
            # Fill red where ratio < 100 (Accumulating inventory)
            ax.fill_between(dates, ratios, baseline,
                              where=ratios <= baseline,
                              interpolate=True,
                              color='lightcoral', alpha=0.4, label='搴撳瓨绉帇鍖?(<100%)')
            # --- End fill_between logic ---

            # Highlight points > 100%
            for i, r_val in enumerate(ratios):
                if r_val > 100:
                    ax.scatter(dates[i], r_val, color='darkred', s=60, zorder=5)
                # Add annotations (with increased font size)
                if i % 2 == 0 or i == len(ratios) - 1:
                   ax.annotate(f'{r_val:.0f}%',
                                 xy=(dates[i], r_val),
                                 xytext=(0, 8),
                                 textcoords='offset points',
                                 ha='center',
                                 fontsize=10)

            # Plot baseline after fills for visibility
            ax.axhline(baseline, color='grey', linestyle='--', linewidth=1.5, label='100%鍩哄噯绾?) 

            # Set labels and title
            ax.set_xlabel('鏃ユ湡', fontsize=12)
            ax.set_ylabel('缁煎悎浜ч攢鐜?(%)', fontsize=12)
            ax.set_title('姣忔棩缁煎悎浜ч攢鐜囪秼鍔?(閿€閲?浜ч噺)', fontsize=16)
            
            # 娣诲姞鏁版嵁鏉ユ簮璇存槑
            plt.figtext(0.5, 0.01, 
                      '鏁版嵁鏉ユ簮锛氫骇鎴愬搧鍏ュ簱鍒楄〃 & 閿€鍞彂绁ㄦ墽琛屾煡璇紙鎺掗櫎瀹㈡埛鍚嶇О涓虹┖銆佸壇浜у搧銆侀矞鍝佺殑璁板綍锛?,
                      ha='center', fontsize=9, color='#555555')
            
            plt.xticks(rotation=45, fontsize=10)
            plt.yticks(fontsize=10)
            ax.set_ylim(bottom=0)
            ax.grid(True, linestyle='--', alpha=0.6)

            # --- Create combined legend --- 
            handles, labels = ax.get_legend_handles_labels()
            # Create custom patches for fill explanation (optional if fill_between label is sufficient)
            # green_patch = mpatches.Patch(color='lightgreen', alpha=0.4, label='娑堣€楀簱瀛樺尯 (>100%)')
            # red_patch = mpatches.Patch(color='lightcoral', alpha=0.4, label='搴撳瓨绉帇鍖?(<100%)')
            # handles.extend([green_patch, red_patch]) # Add patches to legend if created
            
            # Use legend handles generated by plot and fill_between
            ax.legend(handles=handles, labels=labels, fontsize=10, loc='best')
            # --- End combined legend --- 

            plt.tight_layout()
            plt.savefig(chart_path, dpi=300)
            plt.close()
            print(f"Production/Sales ratio chart saved to {chart_path}")
            return chart_path
        except Exception as e:
            print(f"Error generating production/sales ratio chart: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_comprehensive_price_chart(self, price_data, output_path=None):
        """
        鐢熸垚缁煎悎鍞环鎶樼嚎鍥?        
        鍙傛暟:
            price_data: DataFrame锛屽寘鍚玣actory(宸ュ巶)銆乨ate(鏃ユ湡)鍜宲rice(浠锋牸)鍒?            output_path: 杈撳嚭鍥剧墖璺緞
        """
        if price_data.empty:
            print("璀﹀憡: 鏃犳硶鐢熸垚缁煎悎鍞环鍥捐〃锛屾暟鎹负绌?)
            return None
        
        if output_path is None:
            output_path = os.path.join(self.output_dir, "comprehensive_price_chart.png")
        
        try:
            # 鍒涘缓鍥捐〃
            plt.figure(figsize=(14, 7))
            
            # 鑾峰彇涓嶅悓鐨勫伐鍘?            factories = price_data['factory'].unique()
            
            # 瀹氫箟涓嶅悓鍘傚鐨勬牱寮?            styles = {
                '鍔犲伐涓€鍘?: {'color': '#1f77b4', 'marker': 'o', 'linestyle': '-', 'linewidth': 2, 'markersize': 6},
                '鍔犲伐浜屽巶': {'color': '#ff7f0e', 'marker': 's', 'linestyle': '-', 'linewidth': 2, 'markersize': 6},
                '琛屼笟锛堟棭鍒涜祫璁級': {'color': '#2ca02c', 'marker': '^', 'linestyle': '--', 'linewidth': 1.5, 'markersize': 5}
            }
            
            # 缁樺埗姣忎釜宸ュ巶鐨勪环鏍兼姌绾垮浘
            for factory in factories:
                factory_data = price_data[price_data['factory'] == factory]
                # 浣跨敤棰勫畾涔夋牱寮忥紝濡傛灉娌℃湁鍒欎娇鐢ㄩ粯璁ゆ牱寮?                style = styles.get(factory, {'color': 'black', 'marker': 'x', 'linestyle': '-', 'linewidth': 1, 'markersize': 4})
                
                plt.plot(
                    factory_data['date'], 
                    factory_data['price'],
                    label=factory,
                    marker=style['marker'],
                    color=style['color'],
                    linestyle=style['linestyle'],
                    linewidth=style['linewidth'],
                    markersize=style['markersize']
                )
                
                # 涓烘瘡涓暟鎹偣娣诲姞浠锋牸鏍囩
                for _, row in factory_data.iterrows():
                    plt.text(
                        row['date'], 
                        row['price'] + 20,  # 绋嶅井涓婄Щ锛岄伩鍏嶉伄鎸?                        f"{row['price']:.0f}",
                        ha='center',
                        va='bottom',
                        fontsize=8,
                        color=style['color']
                    )
            
            # 璁剧疆鍥捐〃鏍囬鍜岃酱鏍囩
            plt.title('缁煎悎鍞环瓒嬪娍鍥?, fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('鏃ユ湡', fontsize=12)
            plt.ylabel('浠锋牸 (鍏?', fontsize=12)
            
            # 璁剧疆x杞存棩鏈熸牸寮?            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m.%d'))
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            
            # 娣诲姞缃戞牸绾?            plt.grid(True, linestyle='--', alpha=0.3)
            
            # 娣诲姞鍥句緥锛屾斁鍦ㄥ彸涓婅
            plt.legend(loc='upper right', frameon=True, fancybox=True, shadow=True, fontsize=10)
            
            # 鏃嬭浆x杞存爣绛句互闃查噸鍙?            plt.xticks(rotation=45)
            
            # 鑷姩璋冩暣甯冨眬
            plt.tight_layout()
            
            # 淇濆瓨鍥捐〃
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"缁煎悎鍞环鍥捐〃宸茬敓鎴? {output_path}")
            return output_path
            
        except Exception as e:
            print(f"鐢熸垚缁煎悎鍞环鍥捐〃鏃跺嚭閿? {str(e)}")
            import traceback
            traceback.print_exc()
            return None 

    def generate_responsive_image(self, standard_image_path, output_dir):
        """涓虹Щ鍔ㄧ鐢熸垚浼樺寲鐗堟湰鐨勫浘鐗?""
        try:
            from PIL import Image
            import os
          
            # 鑾峰彇鍘熷浘璺緞
            base_name = os.path.basename(standard_image_path)
            file_name, file_ext = os.path.splitext(base_name)
          
            # 鐢熸垚绉诲姩绔増鏈矾寰?            mobile_path = os.path.join(output_dir, f"{file_name}_mobile{file_ext}")
          
            # 浣跨敤PIL鎵撳紑鍥剧墖
            img = Image.open(standard_image_path)
          
            # 鑾峰彇鍘熷灏哄
            width, height = img.size
          
            # 绉诲姩绔昂瀵革紙淇濇寔瀹介珮姣旓級
            mobile_width = 600  # 閫傚悎澶у鏁扮Щ鍔ㄨ澶?            mobile_height = int(height * (mobile_width / width))
          
            # 璋冩暣澶у皬骞朵繚瀛?            mobile_img = img.resize((mobile_width, mobile_height), Image.LANCZOS) # Use Image.LANCZOS for high quality resize
            mobile_img.save(mobile_path, quality=85, optimize=True)
          
            return mobile_path
        except ImportError:
            print("Pillow library not found. Skipping responsive image generation. Install with: pip install Pillow")
            return standard_image_path # Return original path if Pillow is missing
        except Exception as e:
            print(f"鐢熸垚鍝嶅簲寮忓浘鍍忓け璐? {e}")
            return standard_image_path


# Example usage (if run directly)
if __name__ == '__main__':
    # Example: Create dummy daily sales data
    dummy_sales_data = {
        datetime(2023, 10, 1): {'volume': 5000, 'avg_price': 15000},
        datetime(2023, 10, 2): {'volume': 5500, 'avg_price': 15200},
        datetime(2023, 10, 3): {'volume': 4800, 'avg_price': 15100},
        datetime(2023, 10, 4): {'volume': 6000, 'avg_price': None}, # Test None price
        datetime(2023, 10, 5): {'volume': 5200, 'avg_price': 'invalid'}, # Test invalid price
        datetime(2023, 10, 6): {'volume': 5800, 'avg_price': 15500},
    }
    # Example: Create dummy ratio data
    dummy_ratio_data = {
        datetime(2023, 10, 1): {'ratio': 95.5},
        datetime(2023, 10, 2): {'ratio': 105.2},
        datetime(2023, 10, 3): {'ratio': 88.0},
        datetime(2023, 10, 4): {'ratio': 110.0},
        datetime(2023, 10, 5): {'ratio': 92.3},
        datetime(2023, 10, 6): {'ratio': 101.8},
    }

    visualizer = DataVisualizer(output_dir='./test_visuals')
    # Generate sales trend chart
    sales_chart = visualizer.generate_daily_sales_trend(dummy_sales_data)
    if sales_chart:
         print(f"Sales chart generated: {sales_chart}")
         # Test responsive image generation
         mobile_sales_chart = visualizer.generate_responsive_image(sales_chart, visualizer.output_dir)
         print(f"Mobile sales chart potentially generated: {mobile_sales_chart}")

    # Generate ratio chart
    ratio_chart_path = os.path.join(visualizer.output_dir, "test_ratio_chart.png")
    ratio_chart = visualizer.generate_production_sales_ratio_chart(dummy_ratio_data, ratio_chart_path)
    if ratio_chart:
         print(f"Ratio chart generated: {ratio_chart}")

    # Add other chart generation tests if needed
    print("Visualization tests completed.") 