# -*- coding: utf-8 -*-
"""
HTML 鐢熸垚宸ュ叿妯″潡
"""
from datetime import datetime
import os
import time
import tempfile
import shutil
import random

def generate_header(title="鍒嗘瀽鎶ュ憡", output_dir="."):
    """鐢熸垚HTML澶撮儴锛屽寘鍚牱寮忓拰瀵艰埅"""
    # Correctly reference image paths relative to the output directory
    # Example: Use os.path.basename if images are in the same dir, or adjust path
    # Assuming images are in the same output_dir as html files for simplicity now.

    # Extract CSS and JS from the original _generate_html_header
    # Note: Ensure all necessary JS functions are included.
    css_styles = """
        :root {
            --primary-color: #1976D2;
            --secondary-color: #03A9F4;
            --success-color: #4CAF50;
            --warning-color: #FFC107;
            --danger-color: #F44336;
            --light-color: #f8f9fa;
            --dark-color: #343a40;
            --border-radius: 8px;
            --box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            --transition: all 0.3s ease;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f7fa;
            margin: 0;
            padding: 0;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .report-header { /* Renamed from .header to avoid conflicts if used elsewhere */
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 30px 20px;
            border-radius: var(--border-radius);
            margin-bottom: 30px;
            box-shadow: var(--box-shadow);
            text-align: center;
        }
        h1, h2, h3, h4 { color: #333; margin-bottom: 15px; }
        .report-header h1 { color: white; margin: 0; font-size: 28px; }
        .report-header p { margin: 10px 0 0; opacity: 0.9; font-size: 14px; }
        .navigation { background-color: var(--dark-color); padding: 10px 0; margin-bottom: 20px; border-radius: var(--border-radius); box-shadow: var(--box-shadow); }
        .navigation ul { list-style: none; text-align: center; padding: 0; margin: 0; }
        .navigation ul li { display: inline-block; margin: 0 15px; }
        .navigation ul li a { color: var(--light-color); text-decoration: none; padding: 8px 15px; border-radius: 4px; transition: background-color 0.3s ease; }
        .navigation ul li a:hover, .navigation ul li a.active { background-color: var(--primary-color); color: white; }

        .section { background: white; margin-bottom: 30px; border-radius: var(--border-radius); box-shadow: var(--box-shadow); overflow: hidden; }
        .section-header { background-color: var(--light-color); padding: 15px 20px; border-bottom: 1px solid #eee; }
        .section-body { padding: 20px; }
        .subsection { margin-bottom: 25px; border-bottom: 1px solid #eee; padding-bottom: 20px; }
        .subsection:last-child { border-bottom: none; margin-bottom: 0; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; border-radius: var(--border-radius); overflow: hidden; }
        th, td { border: 1px solid #eee; padding: 12px; text-align: left; }
        th { background-color: var(--light-color); font-weight: 600; position: sticky; top: 0; z-index: 10; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        tr:hover { background-color: #f1f1f1; }
        .warning { color: var(--danger-color); font-weight: bold; }
        .highlight { background-color: rgba(255, 193, 7, 0.2); }
        .summary { background-color: #e8f4fd; padding: 15px; border-radius: var(--border-radius); border-left: 4px solid var(--primary-color); max-height: 200px; overflow-y: auto; }
        img { max-width: 100%; height: auto; margin: 15px 0; border-radius: var(--border-radius); box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .filter-container { margin-bottom: 20px; padding: 15px; background-color: var(--light-color); border-radius: var(--border-radius); display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
        .filter-container label { margin-right: 8px; font-weight: 600; color: #555; }
        .filter-container select, .filter-container input { padding: 8px 12px; margin-right: 15px; border-radius: 4px; border: 1px solid #ddd; min-width: 150px; background-color: white; }
        .filter-container select:focus, .filter-container input:focus { outline: none; border-color: var(--primary-color); box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1); }
        .filter-container button { padding: 8px 15px; background-color: var(--primary-color); color: white; border: none; border-radius: 4px; cursor: pointer; transition: var(--transition); }
        .filter-container button:hover { background-color: #1565C0; transform: translateY(-2px); }
        .inventory-table-container, .sales-table-container, .detail-table-container { /* Consolidated common styles */
            max-height: 300px; /* Default height, can be overridden */
            overflow-y: auto;
            margin-bottom: 20px;
            border-radius: var(--border-radius);
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid #eee;
        }
        .inventory-summary { display: flex; flex-wrap: wrap; justify-content: space-between; margin-bottom: 20px; gap: 15px; }
        .inventory-card { background-color: white; border-radius: var(--border-radius); padding: 20px; flex: 1; min-width: 200px; box-shadow: var(--box-shadow); transition: var(--transition); border-top: 4px solid var(--primary-color); }
        .inventory-card:hover { transform: translateY(-5px); }
        .inventory-card h4 { margin-top: 0; color: #555; font-size: 16px; }
        .inventory-card .value { font-size: 28px; font-weight: bold; color: var(--primary-color); margin: 10px 0; }
        .inventory-search, .sales-search, .detail-search { /* Consolidated common styles */
            margin-bottom: 15px;
            position: relative;
        }
        .inventory-search input, .sales-search input, .detail-search input { /* Consolidated common styles */
            padding: 10px 15px 10px 40px;
            width: 100%;
            border: 1px solid #ddd;
            border-radius: var(--border-radius);
            font-size: 14px;
        }
        .inventory-search:before, .sales-search:before, .detail-search:before { /* Consolidated common styles */
            content: "馃攳";
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #999;
        }
        .ratio-chart-container { display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 20px; }
        .ratio-chart { flex: 1; min-width: 300px; background-color: white; padding: 20px; border-radius: var(--border-radius); box-shadow: var(--box-shadow); }
        .status-badge { display: inline-block; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 600; }
        .status-balanced { background-color: rgba(25, 118, 210, 0.1); color: var(--primary-color); }
        .status-surplus { background-color: rgba(244, 67, 54, 0.1); color: var(--danger-color); }
        .status-shortage { background-color: rgba(76, 175, 80, 0.1); color: var(--success-color); }
        .data-card { background-color: white; border-radius: var(--border-radius); padding: 20px; margin-bottom: 20px; box-shadow: var(--box-shadow); }
        .data-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #eee; }
        .data-card-title { font-size: 18px; font-weight: 600; color: #333; margin: 0; }
        .data-card-body { padding: 10px 0; }
        .sales-container { width: 100%; margin-bottom: 15px; }
        .sales-flex { display: flex; flex-wrap: wrap; margin: -5px; }
        .sales-flex-item { flex: 0 0 calc(20% - 10px); margin: 5px; box-sizing: border-box; }
        .sales-card { background-color: #f5f5f5; border-radius: 4px; padding: 8px 10px; cursor: pointer; transition: 0.2s; position: relative; border: 1px solid #e0e0e0; box-shadow: 0 1px 2px rgba(0,0,0,0.03); height: 100%; }
        .sales-card:hover { background-color: #eaeaea; box-shadow: 0 2px 4px rgba(0,0,0,0.08); }
        .sales-card.active { background-color: #e0e0e0; } /* Highlight active card */
        .sales-card-header { display: flex; justify-content: space-between; align-items: center; }
        .sales-card-header h4 { margin: 0; font-size: 13px; color: #333; font-weight: 600; }
        .toggle-icon { font-size: 11px; color: #777; transition: transform 0.3s ease; }
        .sales-card.active .toggle-icon { transform: rotate(180deg); }
        .sales-card-body { margin-top: 5px; }
        .sales-card-body p { margin: 3px 0 0 0; font-size: 12px; color: #555; line-height: 1.3; }
        .card-hint { font-size: 11px; color: #999; text-align: center; margin-top: 5px; }

        /* Panel styles for ratio and sales details */
        .ratio-panel, .sales-panel {
            display: none; /* Hidden by default */
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-top: 10px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            padding: 15px; /* Add padding */
        }
        .ratio-panel.active, .sales-panel.active {
             display: block; /* Shown when active */
        }
        .ratio-panel-header, .sales-panel-header { /* Shared styles for panel headers */
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 10px;
            margin-bottom: 10px;
            border-bottom: 1px solid #eee;
        }
         .ratio-panel-header h4, .sales-panel-header h4 { margin: 0; font-size: 16px; }
         .ratio-panel-controls, .sales-panel-controls { display: flex; align-items: center; gap: 10px;}
        .search-input { /* Specific styling for search inputs in panels */
            padding: 5px 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 13px;
        }
        .close-button { /* Styling for close buttons in panels */
            background: none;
            border: none;
            font-size: 16px;
            cursor: pointer;
            color: #666;
            padding: 0 5px;
        }
        .close-button:hover { color: #333; }

        .ratio-panel .sales-table-container, .sales-panel .sales-table-container { /* Panel specific table container */
             max-height: 400px;
             border: 1px solid #eee; /* Add border */
             border-radius: 4px;
         }
        .ratio-panel table td, .ratio-panel table th,
        .sales-panel table td, .sales-panel table th { /* Compact table cells for panels */
            padding: 6px 8px;
            font-size: 13px;
        }

        /* Value highlighting */
        .high-value { color: var(--success-color); font-weight: bold; }
        .medium-value { color: var(--warning-color); font-weight: bold; }
        .low-value { color: var(--danger-color); font-weight: bold; }

        /* Collapsible button/content (if needed later) */
        .collapsible-button { /* ... styles ... */ }
        .collapsible-content { /* ... styles ... */ }

        /* Total row style */
        .total-row { background-color: #f0f8ff; border-top: 2px solid #ddd; font-weight: bold; }
        .total-row td { padding: 8px; }
        .text-right { text-align: right; } /* Utility class */

        /* Responsive */
        @media (max-width: 992px) { /* Adjust breakpoint if needed */
             .sales-flex-item { flex: 0 0 calc(25% - 10px); } /* 4 cards per row */
        }
        @media (max-width: 768px) {
            .container { padding: 10px; }
            .report-header { padding: 20px 15px; }
            .inventory-summary { flex-direction: column; }
            .inventory-card { width: 100%; }
            .filter-container { flex-direction: column; align-items: flex-start; }
            .filter-container select, .filter-container input { width: 100%; margin-right: 0; margin-bottom: 10px; }
            .sales-flex-item { flex: 0 0 calc(50% - 10px); } /* 2 cards per row */
            .navigation ul li { margin: 0 5px; } /* Reduce nav spacing */
             .navigation ul li a { padding: 6px 10px; }
        }
         @media (max-width: 576px) {
             .sales-flex-item { flex: 0 0 calc(100% - 10px); } /* 1 card per row */
         }

        /* --- Added Mobile Responsive Styles --- */
        @media (max-width: 768px) {
            .container {
                padding: 0 10px;
                margin: 10px auto;
            }

            /* 琛ㄦ牸瀹瑰櫒閫傞厤 */
            .detail-table-container, .inventory-table-container, .sales-table-container {
                width: 100%;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch; /* 鏇撮『婊戠殑iOS婊氬姩 */
            }

            /* 琛ㄦ牸鍐呭绮剧畝 */
            table th, table td {
                padding: 6px 8px;
                font-size: 0.85em;
            }

            /* 璋冩暣鍥捐〃澶у皬 */
            img.chart, img.img-fluid {
                max-width: 100%;
                height: auto;
            }

            /* 鍗＄墖甯冨眬璋冩暣 */
            .sales-flex-item, .inventory-card {
                width: 100%;
                margin-bottom: 10px;
            }

            /* 鍑忓皯闈㈡澘濉厖 */
            .data-card-body, .section-body {
                padding: 10px;
            }

            /* 纭繚鎸夐挳澶у皬閫備腑 */
            .btn {
                padding: 6px 12px;
                font-size: 0.9em;
            }

            /* --- Responsive Stacking Table for Price Volatility --- */
            .stacking-table-mobile {
                border: none; /* Remove table border */
                width: 100%;
            }
            .stacking-table-mobile thead {
                display: none; /* Hide table header on mobile */
            }
            .stacking-table-mobile tr {
                display: block; /* Make rows behave like blocks */
                margin-bottom: 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                background-color: #fff; /* Give each 'row' a background */
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            .stacking-table-mobile td {
                display: block; /* Make cells behave like blocks */
                width: 100%;
                box-sizing: border-box;
                text-align: right; /* Align data value to the right */
                padding-left: 45%; /* Make space for the label */
                position: relative; /* Needed for absolute positioning of the label */
                border-bottom: 1px dotted #eee; /* Separator between 'cells' */
                padding-top: 5px;
                padding-bottom: 5px;
                min-height: 24px; /* Ensure minimum height */
            }
            .stacking-table-mobile td:last-child {
                border-bottom: none; /* No border for the last 'cell' in a block */
            }
            .stacking-table-mobile td::before {
                content: attr(data-label); /* Use the data-label attribute as content */
                position: absolute;
                left: 10px; /* Position the label */
                width: calc(45% - 15px); /* Control label width */
                padding-right: 10px;
                text-align: left; /* Align label text to the left */
                font-weight: bold;
                white-space: nowrap; /* Prevent label wrap */
                color: #333;
            }
            /* --- End Responsive Stacking Table --- */

        }
        /* --- End Added Mobile Responsive Styles --- */

        /* 澧炲己琛ㄦ牸婊氬姩瀹瑰櫒锛岀‘淇濋€傞厤灏忓睆骞?*/
        .table-responsive {
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            max-width: 100vw; /* Changed from 100% to 100vw for clarity */
        }
    """

    javascript = """
        // Global function: Toggle ratio/sales detail panel visibility and card active state
        function toggleDetailPanel(panelType, dateStr, event) {
            var panelId = panelType + "Panel_" + dateStr; // e.g., "ratioPanel_2023-10-26" or "salesPanel_2023-10-26"
            var panel = document.getElementById(panelId);
            if(!panel) return; // Element not found

            var clickedCard = event.currentTarget; // The card that was clicked
            var allPanels = document.querySelectorAll('.' + panelType + '-panel'); // Select all panels of the same type
            var allCards = clickedCard.closest('.sales-flex').querySelectorAll('.sales-card'); // Find sibling cards

            // If the clicked panel is already active, hide it and deactivate card
            if (panel.classList.contains('active')) {
                panel.classList.remove('active');
                panel.style.display = "none";
                if(clickedCard) clickedCard.classList.remove('active');
            } else {
                // Hide all other panels of the same type and deactivate their cards
                allPanels.forEach(function(p) {
                    if (p.id !== panelId && p.classList.contains('active')) {
                        p.classList.remove('active');
                        p.style.display = "none";
                    }
                });
                 allCards.forEach(function(card) {
                     card.classList.remove('active');
                 });

                // Show the clicked panel and activate its card
                panel.classList.add('active');
                panel.style.display = "block"; // Make sure display is set to block
                if(clickedCard) clickedCard.classList.add('active');
            }

            // Prevent event bubbling (optional, but often good practice)
            if(event) event.stopPropagation();
        }

        // Global function: Search within a table inside a panel
        function searchTableInPanel(tableId, inputId) {
            const input = document.getElementById(inputId);
            if (!input) return;
            
            const filter = input.value.toUpperCase();
            const table = document.getElementById(tableId);
            if (!table) return;
            
            const tr = table.getElementsByTagName("tr");
            const totalRow = Array.from(tr).find(row => row.classList.contains('total-row'));
            
            // 濡傛灉娌℃湁杈撳叆绛涢€夋潯浠讹紝纭繚鎵€鏈夐潪鍚堣琛岄兘鍙
            if (!filter) {
                for (let i = 0; i < tr.length; i++) {
                    if (i === 0 || tr[i].classList.contains('total-row')) continue;
                    tr[i].style.display = ""; // 纭繚琛屽彲瑙?                }
                // **閲嶈**: 濡傛灉娌℃湁绛涢€夛紝涓嶄慨鏀瑰悎璁¤锛屼繚鎸佸叾鍘熷鐘舵€併€?                // 闇€瑕佺‘淇漃ython鐢熸垚鐨凥TML鍖呭惈姝ｇ‘鐨勫師濮嬪悎璁°€?                return; 
            }
            
            // 鏍规嵁琛ㄦ牸ID鍒ゆ柇琛ㄦ牸绫诲瀷
            const isRatioTable = tableId.includes('ratioTable');
            const isSalesTable = tableId.includes('salesTable');
            
            // 鍒濆鍖栧悎璁″€?            let volumeTotal = 0;      // 閫氱敤锛氶攢閲?鏁伴噺鍚堣
            let productionTotal = 0;  // 浜ч攢鐜囪〃锛氫骇閲忓悎璁?            let amountTotal = 0;      // 閿€鍞〃锛氭棤绋庨噾棰濆悎璁?            let visibleRowCount = 0;
            
            // 澶勭悊鏁版嵁琛?(杩囨护骞剁疮鍔?
            for (let i = 0; i < tr.length; i++) {
                if (i === 0 || tr[i].classList.contains('total-row')) continue; // 璺宠繃琛ㄥご鍜屽悎璁¤
                
                const td = tr[i].getElementsByTagName("td");
                let txtValue = "";
                let visible = false;
                
                // 妫€鏌ユ墍鏈夊崟鍏冩牸鏄惁鍖归厤绛涢€夋潯浠?                for (let j = 0; j < td.length; j++) {
                    if (td[j]) {
                        txtValue = td[j].textContent || td[j].innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                            visible = true;
                            break;
                        }
                    }
                }
                
                tr[i].style.display = visible ? "" : "none"; // 鏍规嵁鍙鎬ц缃樉绀?                
                // 濡傛灉琛屽彲瑙侊紝绱姞鏁版嵁鍒板悎璁?                if (visible) {
                    visibleRowCount++;
                    try {
                        if (isRatioTable && td.length >= 3) {
                            // 浜ч攢鐜囪〃: 绱姞閿€閲?td[1])鍜屼骇閲?td[2])
                            let salesVal = parseFloat(td[1].textContent.replace(/,/g, '')) || 0;
                            let prodVal = parseFloat(td[2].textContent.replace(/,/g, '')) || 0;
                            volumeTotal += salesVal;
                            productionTotal += prodVal;
                        } else if (isSalesTable && td.length >= 3) {
                            // 閿€鍞槑缁嗚〃: 绱姞閿€閲?td[1])鍜屾棤绋庨噾棰?td[2])
                            let salesVol = parseFloat(td[1].textContent.replace(/,/g, '')) || 0;
                            let salesAmount = parseFloat(td[2].textContent.replace(/,/g, '')) || 0;
                            volumeTotal += salesVol;
                            amountTotal += salesAmount;
                        }
                    } catch (e) {
                        console.error("澶勭悊鏁板€艰繘琛屽悎璁℃椂鍑洪敊:", e, tr[i]);
                    }
                }
            }
            
            // 鏇存柊鍚堣琛屾暟鎹?(浠呭綋鏈夌瓫閫夋潯浠舵椂)
            if (totalRow && filter) {
                const totalTds = totalRow.getElementsByTagName("td");
                if (isRatioTable && totalTds.length >= 4) {
                    totalTds[1].innerHTML = '<strong>' + volumeTotal.toLocaleString('en-US', {maximumFractionDigits: 0}) + '</strong>'; // 閿€閲忓悎璁?                    totalTds[2].innerHTML = '<strong>' + productionTotal.toLocaleString('en-US', {maximumFractionDigits: 0}) + '</strong>'; // 浜ч噺鍚堣
                    const ratio = productionTotal > 0 ? (volumeTotal / productionTotal * 100).toFixed(1) : "0.0";
                    totalTds[3].innerHTML = '<strong>' + ratio + '%</strong>'; // 浜ч攢鐜?                } else if (isSalesTable && totalTds.length >= 4) {
                    totalTds[1].innerHTML = '<strong>' + volumeTotal.toLocaleString('en-US', {maximumFractionDigits: 0}) + '</strong>'; // 閿€閲忓悎璁?                    totalTds[2].innerHTML = '<strong>' + amountTotal.toLocaleString('en-US', {maximumFractionDigits: 0}) + '</strong>'; // 鏃犵◣閲戦鍚堣
                    // 璁＄畻鍚◣鍗曚环 (鍏?鍚?
                    let avgPrice = 0;
                    if (volumeTotal > 0) {
                        // 鍋囪 volumeTotal 鍗曚綅鏄?kg, amountTotal 鏄厓
                        avgPrice = (amountTotal / volumeTotal) * 1.09 * 1000; 
                    }
                    totalTds[3].innerHTML = '<strong>' + avgPrice.toLocaleString('en-US', {maximumFractionDigits: 0}) + '</strong>'; // 鍚◣鍗曚环
                }
            }
        }

        // General purpose table search function (for tables not in panels)
        function searchTable(tableId, searchInputId) {
             var input = document.getElementById(searchInputId);
             var filter = input.value.toUpperCase();
             var table = document.getElementById(tableId);
             var tr = table.getElementsByTagName("tr");

             for (var i = 1; i < tr.length; i++) { // Start from 1 to skip header
                 var found = false;
                 var td = tr[i].getElementsByTagName("td");
                 for (var j = 0; j < td.length; j++) {
                     if (td[j]) {
                         var txtValue = td[j].textContent || td[j].innerText;
                         // Improved search: check if any cell contains the filter text
                         if (txtValue.toUpperCase().indexOf(filter) > -1) {
                             found = true;
                             break; // Exit inner loop once found in a row
                         }
                     }
                 }
                 tr[i].style.display = found ? "" : "none";
             }
         }

        // Specific function wrappers for onclick events to maintain compatibility
         function toggleRatioPanel(dateStr, event) {
             toggleDetailPanel('ratio', dateStr, event);
         }
         function searchProducts(dateStr) {
            // Assuming the input id is searchInput-dateStr and table id is productTable-dateStr based on original code
            var input = document.getElementById("searchInput-" + dateStr);
            var table = document.getElementById("productTable-" + dateStr);
            if (!input || !table) return;

            var filter = input.value.toUpperCase();
            var tr = table.getElementsByTagName("tr");

            for (var i = 1; i < tr.length; i++) { // Skip header row
                var td = tr[i].getElementsByTagName("td")[0]; // Search first column (Product Name)
                if (td) {
                    var txtValue = td.textContent || td.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                    } else {
                        tr[i].style.display = "none";
                    }
                }
            }
        }
         function toggleSalesPanel(dateStr, event) {
             toggleDetailPanel('sales', dateStr, event);
         }
         function searchSales(dateStr) {
             searchTableInPanel('sales', dateStr);
         }
        function searchInventory() {
            searchTable('inventoryTable', 'inventorySearch');
        }
        // Add search functions for other tables if needed, e.g., searchAbnormal, searchInconsistent, searchConflict, searchComparison
        // They can all use the generic searchTable function:
        // function searchAbnormal() { searchTable('abnormalTable', 'abnormalSearch'); }
        // function searchInconsistent() { searchTable('inconsistentTable', 'inconsistentSearch'); }
        // function searchConflict() { searchTable('conflictTable', 'conflictSearch'); }
        // function searchComparison() { searchTable('comparisonTable', 'comparisonSearch'); }

        // Add DOMContentLoaded listener if needed for initializations from original footer script
        // document.addEventListener('DOMContentLoaded', function() { /* ... */ });

        // --- Added Mobile Enhancement Script ---
        document.addEventListener('DOMContentLoaded', function() {
            // 娣诲姞琛ㄦ牸婊戝姩鎻愮ず
            const tableContainers = document.querySelectorAll('.table-responsive');

            tableContainers.forEach(container => {
                // Check if the table actually needs to scroll
                if (container.scrollWidth > container.clientWidth) {
                    // 鍒涘缓婊戝姩鎻愮ず鍏冪礌
                    const hint = document.createElement('div');
                    hint.className = 'swipe-hint';
                    hint.innerHTML = '<i class="bi bi-arrow-left-right"></i> 宸﹀彸婊戝姩鏌ョ湅鏇村';
                    // Use inline styles as provided, ensure Bootstrap Icons are loaded if using bi-* classes
                    hint.style.cssText = 'text-align: center; color: #666; font-size: 0.8em; padding: 5px; margin-top: -10px; margin-bottom: 5px;'; // Adjusted margins

                    // 鎻掑叆鍒拌〃鏍煎鍣ㄤ箣鍓?                    container.parentNode.insertBefore(hint, container);

                    // 鐩戝惉婊氬姩锛屾粴鍔ㄥ悗闅愯棌鎻愮ず
                    container.addEventListener('scroll', function() {
                        hint.style.display = 'none';
                    }, {once: true});  // 鍙Е鍙戜竴娆?                }
            });

            // 閫傞厤琛ㄦ牸鍒楀 (Optional: 'auto' might not always be desired, consider carefully)
            const tables = document.querySelectorAll('.mobile-friendly-table'); // Target tables with this class
            if (window.innerWidth <= 768) {
                tables.forEach(table => {
                    // 鏍规嵁鍐呭鑷姩璋冩暣鍒楀 - Use with caution, might make narrow columns too wide
                    // table.style.tableLayout = 'auto';
                    console.log("Adjusting table layout for mobile:", table.id); // Log for debugging
                });
            }

            // --- Add other DOMContentLoaded initializations below if needed ---

        });
        // --- End Added Mobile Enhancement Script ---
    """

    # Get current time for the header (if needed, or use footer)
    current_time_header = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <style>
        {css_styles}
    </style>
    <script>
        {javascript}
    </script>
</head>
<body>
    <div class="container">
        <div class="report-header">
            <h1>鏄ラ洩椋熷搧鐢熷搧浜ч攢鍒嗘瀽鎶ュ憡</h1>
            <!-- <p>鐢熸垚鏃堕棿: {current_time_header}</p> -->
            <p>鎶ュ憡浣滆€? quzhupeng@springsnow.cn</p>
        </div>
"""

def generate_navigation(active_page="index"):
    """鐢熸垚瀵艰埅鏍廐TML"""
    nav_items = {
        "index": {"name": "鍒嗘瀽鎽樿", "url": "index.html"},
        "inventory": {"name": "搴撳瓨鎯呭喌", "url": "inventory.html"},
        "ratio": {"name": "浜ч攢鐜囧垎鏋?, "url": "ratio.html"},
        "sales": {"name": "閿€鍞儏鍐?, "url": "sales.html"},
        "details": {"name": "璇︾粏鏁版嵁", "url": "details.html"},
        "price_volatility": {"name": "浠锋牸娉㈠姩", "url": "price_volatility.html"},
        "industry": {"name": "鍗撳垱璧勮", "url": "industry.html"}
    }
    nav_html = '<nav class="navigation"><ul>'
    for key, item in nav_items.items():
        active_class = 'active' if key == active_page else ''
        nav_html += f'<li><a href="{item["url"]}" class="{active_class}">{item["name"]}</a></li>'
    nav_html += '</ul></nav>'
    return nav_html

def generate_footer():
    """鐢熸垚HTML椤佃剼"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"""
            <div class="section">
                <div class="section-header">
                    <h2>鎶ュ憡璇存槑</h2>
                </div>
                <div class="section-body">
                    <p>鏈姤鍛婃暟鎹潵婧愪簬浼佷笟鍐呴儴绯荤粺銆傛姤鍛婁腑鐨勫垎鏋愮粨鏋滀粎渚涘弬鑰冿紝鍏蜂綋涓氬姟鍐崇瓥璇风粨鍚堝疄闄呮儏鍐点€?/p>
                    <p>濡傛湁浠讳綍闂鎴栧缓璁紝璇疯仈绯籫uanlibu@springsnow.cn</p>
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
              
              // 琛ㄦ牸鎼滅储鍑芥暟 - 鐢ㄤ簬涓€鑸〃鏍兼悳绱?              function searchTable(tableId, inputId) {{
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
              
              // 鍒囨崲浜ч攢鐜囨槑缁嗛潰鏉?              function toggleRatioPanel(dateStr, event) {{
                  if (event) event.stopPropagation();
                  const panelId = `ratioPanel_${{dateStr}}`;
                  togglePanel(panelId, null);
              }}
              
              // 鍒囨崲閿€鍞槑缁嗛潰鏉?              function toggleSalesPanel(dateStr, event) {{
                  if (event) event.stopPropagation();
                  const panelId = `salesPanel_${{dateStr}}`;
                  togglePanel(panelId, null);
              }}
        </script>
    </body>
</html>
"""

def write_html_report(html_content, filename, output_dir):
    """灏咹TML鍐呭鍐欏叆鏂囦欢"""
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, filename)
    
    # 寮哄埗鍨冨溇鍥炴敹锛屽皾璇曢噴鏀炬枃浠跺彞鏌?    import gc
    gc.collect()
    
    # 閲嶈瘯鏈哄埗
    max_retries = 3
    retry_delay = 1  # 寤惰繜1绉?    
    for attempt in range(max_retries):
        try:
            # 浣跨敤涓存椂鏂囦欢鏂瑰紡鍐欏叆锛岄伩鍏嶇洿鎺ュ啓鍏ユ椂鐨勬枃浠堕攣瀹氶棶棰?            temp_fd, temp_path = tempfile.mkstemp(suffix='.html', prefix=f"{filename.split('.')[0]}_temp_", dir=output_dir)
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as temp_file:
                temp_file.write(html_content)
            
            # 濡傛灉鐩爣鏂囦欢瀛樺湪锛屽皾璇曞垹闄ゅ畠
            if os.path.exists(report_path):
                try:
                    os.remove(report_path)
                except PermissionError:
                    # 濡傛灉涓嶈兘鍒犻櫎锛屽皾璇曢噸鍛藉悕鍘熸枃浠?                    backup_name = f"{filename.split('.')[0]}_{int(time.time())}_{random.randint(1000, 9999)}.bak.html"
                    backup_path = os.path.join(output_dir, backup_name)
                    os.rename(report_path, backup_path)
                    print(f"鏃犳硶鍒犻櫎鍘熸枃浠讹紝宸插皢鍏堕噸鍛藉悕涓? {backup_name}")
            
            # 灏嗕复鏃舵枃浠跺鍒跺埌鐩爣璺緞
            shutil.copy2(temp_path, report_path)
            os.remove(temp_path)  # 鍒犻櫎涓存椂鏂囦欢
            
            print(f"鎶ュ憡宸茬敓鎴? {report_path}")
            # 濡傛灉鎴愬姛鍐欏叆锛岃緭鍑洪〉闈㈡垚鍔熺敓鎴愭秷鎭?            if filename == "index.html":
                print(f"index.html 椤甸潰宸茬敓鎴愬湪 {output_dir}")
            elif filename == "details.html":
                print(f"details.html 椤甸潰宸茬敓鎴愬湪 {output_dir}")
            elif filename == "price_volatility.html":
                print(f"price_volatility.html generated in {output_dir}")
            elif filename == "industry.html":
                print(f"industry.html 椤甸潰宸茬敓鎴愬湪 {output_dir}")
            
            return report_path
            
        except Exception as e:
            print(f"鍐欏叆鎶ュ憡 {filename} 鏃跺彂鐢熼敊璇?(灏濊瘯 {attempt+1}/{max_retries}): {str(e)}")
            import traceback
            traceback.print_exc()
            
            if attempt < max_retries - 1:
                print(f"灏嗗湪 {retry_delay} 绉掑悗閲嶈瘯...")
                time.sleep(retry_delay)
                retry_delay *= 2  # 澧炲姞涓嬩竴娆＄瓑寰呮椂闂?            else:
                print(f"鏃犳硶鍐欏叆鎶ュ憡 {filename}锛岃揪鍒版渶澶ч噸璇曟鏁般€?)
    
    return None

# Helper function to generate image tags safely
def generate_image_tag(image_filename, alt_text="", css_class="img-fluid"):
    """Generates an <img> tag, assuming image is relative to HTML file."""
    # In a multi-file setup, ensure the image path is correct relative to the HTML file.
    # If images and HTML are in the same output dir, just the filename is needed.
    return f'<img src="{image_filename}" alt="{alt_text}" class="{css_class}">' 