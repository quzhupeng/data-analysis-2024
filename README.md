# Price Analysis Report Generation System

## Project Overview

This system automates the processing of various Excel spreadsheets to generate a series of interlinked HTML reports. These reports are designed to provide business leaders with actionable insights for data-driven decision-making, covering aspects like pricing strategy, sales performance, inventory management, and industry trends.

**Key Features:**

*   **Automated Data Ingestion:** Processes data from multiple Excel files, including:
    *   Price adjustment tables
    *   Inventory summaries (receipts, dispatches, stock)
    *   Sales invoices
    *   Finished goods warehousing data
    *   Competitor pricing comparisons
    *   Industry price benchmarks
*   **Comprehensive Data Analysis:** Performs various analyses such as price change detection, sales ratio calculations, sales trend analysis, and data consistency checks.
*   **HTML Report Generation:** Creates a suite of user-friendly HTML reports with data visualizations.
*   **Modular Design:** Built with Python, utilizing libraries like Pandas for data manipulation.

**Target Audience:**

*   Business leaders and managers requiring insights into sales, inventory, and pricing.

## How it Works (High-Level)

The system follows a data pipeline:

1.  **Data Loading:** Excel files from configured paths are loaded using `data_loader.py`.
2.  **Data Processing & Analysis:** The loaded data is cleaned, processed, and analyzed by `analyzer.py` to identify trends, anomalies, and key metrics.
3.  **Visualization:** `visualizer.py` generates charts and graphs for the reports (though some visualizations are embedded directly in report generation logic).
4.  **Report Generation:** Modules like `index_report.py`, `sales_report.py`, `inventory_report.py`, etc., along with `html_utils.py`, compile the data and visualizations into HTML files.
5.  **Main Orchestration:** `main.py` controls the overall workflow, from data loading to the final report generation.

## Generated Reports

The system generates the following key HTML reports, accessible via an `index.html` dashboard:

*   **Summary Dashboard (`index.html`):** Provides a high-level overview of key performance indicators, price anomalies, and sales-to-production ratios.
*   **Inventory Analysis (`inventory.html`):** Displays current inventory status and trends.
*   **Sales Performance (`sales.html`):** Shows sales trends and integrated sales price analysis.
*   **Production/Sales Ratio (`ratio.html`):** Analyzes the ratio of production to sales, highlighting potential imbalances.
*   **Price Volatility (`price_volatility.html`):** Details price adjustments and comparisons with competitor data.
*   **Industry Trends (`industry.html`):** Tracks and displays relevant industry price benchmarks.
*   **Detailed Data Views (`details.html`):** Offers granular views of sales and production/sales ratio data.

## Setup and Usage

**Prerequisites:**

*   Python 3.x
*   Pandas library (`pip install pandas`)

**Configuration:**

1.  Data file paths are configured in `config.py`. You **must** update these paths to point to your local Excel files before running the system.
    *   `DATA_PATH`: Path to the price adjustment Excel file.
    *   `INVENTORY_PATH`: Path to the inventory summary Excel file.
    *   `SALES_PATH`: Path to the sales invoice Excel file.
    *   `PRODUCTION_PATH`: Path to the finished goods warehousing Excel file.
    *   `COMPREHENSIVE_PRICE_DIR` and `COMPREHENSIVE_PRICE_PATTERN`: Directory and pattern for comprehensive sales price files.
    *   Paths for industry price data (e.g., `CHICKEN_PRICE_PATH`, `RAW_CHICKEN_PRICE_PATH`, etc.).
2.  The default output directory for reports is `output_html_report/` (relative to the project root), also configurable in `config.py`.

**Running the System:**

1.  Navigate to the project's root directory in your terminal.
2.  Run the main script:
    ```bash
    python main.py
    ```
3.  This will process the data and generate/update the HTML reports in the `output_html_report/` directory.

**Accessing Reports:**

*   Open `output_html_report/index.html` in your web browser to view the main dashboard and navigate to other reports.

## Future Enhancements Plan (Roadmap)

This section outlines potential areas for optimizing the system and enhancing its capabilities, particularly focusing on UI/UX and overall robustness, to better serve business leaders with professional, clear, and actionable insights.

**Current State & Achievable Goals:**

The system currently excels at automatically processing Excel data and generating a comprehensive suite of static HTML reports. This provides a valuable, automated foundation for data aggregation, initial visualization, and identifying key business metrics. The goal of future enhancements is to build upon this foundation to create a more dynamic, user-friendly, and robust analytical tool.

**Areas for Optimization & Improvement:**

1.  **UI/UX Enhancements:**
    *   **Interactivity:** Transition from static HTML to dynamic reports.
        *   *Suggestion:* Implement interactive charts (e.g., using Chart.js, Plotly.js, or similar JavaScript libraries, potentially integrated via a Python web framework like Dash or Flask). This would allow features like hover-to-see-data, clickable legends, drill-down capabilities, and dynamic filtering directly on charts.
        *   *Suggestion:* Introduce sortable and filterable tables within the HTML reports for easier data exploration.
    *   **Responsiveness & Modern Aesthetics:**
        *   *Suggestion:* Enhance the existing CSS or adopt a modern CSS framework (like Bootstrap, Tailwind CSS) to ensure a fully responsive design that adapts seamlessly to desktops, tablets, and mobile devices.
        *   *Suggestion:* Undertake a design refresh focusing on cleaner layouts, improved typography, a cohesive and professional color palette, and potentially company branding elements.
    *   **Improved Navigation & Dashboarding:**
        *   *Suggestion:* Redesign the `index.html` to be a more powerful dashboard, offering a clearer overview of all reports and key metrics at a glance with intuitive navigation to detailed sections.
        *   *Suggestion:* Implement breadcrumbs or clearer back-navigation within nested reports.

2.  **Performance Optimization:**
    *   **Efficient Data Handling:**
        *   *Suggestion:* For very large Excel files, investigate optimizing Pandas usage (e.g., reading only necessary sheets/columns, explicitly defining data types on load to reduce memory).
        *   *Suggestion:* Explore caching mechanisms for processed data or generated report components, especially for data that doesn't change frequently, to speed up report loading times.
    *   **Report Generation Speed:**
        *   *Suggestion:* Profile the report generation process to identify bottlenecks and optimize slow-running sections of the Python code.

3.  **Configuration & Deployment:**
    *   **Flexible Configuration:**
        *   *Suggestion:* Replace hardcoded file paths in `config.py` with a more user-friendly and flexible configuration system. Options include using an external configuration file (e.g., `config.ini`, `config.json`, `YAML`) or environment variables. This would make it easier for non-developers to update paths.
    *   **Easier Deployment & Accessibility:**
        *   *Suggestion:* For broader access beyond running a Python script, consider packaging the application (e.g., using PyInstaller) to create a standalone executable.
        *   *Suggestion:* Alternatively, transform the project into a web application using a framework like Flask or Dash, allowing it to be hosted on a central server for team access via a web browser.

4.  **Modularity, Maintainability & Robustness:**
    *   **Code Refactoring:**
        *   *Suggestion:* As new features are added, continuously refactor the Python code. For instance, the `main.py` script could be further modularized, and report generation logic could be encapsulated into more reusable classes or functions.
    *   **Comprehensive Logging:**
        *   *Suggestion:* Implement a structured logging framework (e.g., Python's `logging` module) throughout the application. This will aid in debugging, monitoring data processing, and understanding errors.
    *   **Enhanced Error Handling:**
        *   *Suggestion:* Improve error handling to provide more informative messages to the user, especially for issues related to data file format errors or missing files.

5.  **Security (Especially if deployed as a Web Application):**
    *   *Suggestion:* If the system evolves into a web application, security considerations will be paramount. This includes input validation, protecting against common web vulnerabilities (XSS, CSRF), and potentially implementing user authentication and authorization if sensitive data is involved.

**Proposed Step-by-Step Implementation (High-Level Phases):**

*   **Phase 1: Foundational UI/UX & Core Report Redesign:**
    *   Select a UI approach (e.g., enhanced static HTML with JS libraries, or a Python web framework like Dash/Flask).
    *   Develop a new responsive layout and style guide.
    *   Redesign one or two key reports (e.g., the Summary Dashboard and Sales Performance report) as a prototype with interactive elements.
*   **Phase 2: Expand Interactivity & Convert Remaining Reports:**
    *   Implement interactive charts and tables across more reports.
    *   Convert the remaining static reports to the new, dynamic UI framework.
    *   Refine navigation and overall user flow.
*   **Phase 3: Configuration, Performance, & Robustness:**
    *   Implement a flexible configuration system (e.g., external config file).
    *   Profile and optimize critical data loading and processing paths.
    *   Integrate comprehensive logging and improve error handling.
*   **Phase 4: Advanced Features & Deployment:**
    *   Explore and implement caching strategies.
    *   If pursuing a web application route, develop necessary features for deployment (e.g., WSGI server setup, containerization with Docker).
    *   Package as a standalone application if that's the preferred deployment model.

This roadmap provides a direction for evolving the Price Analysis Report Generation System into an even more powerful and user-centric tool. The specific order and priority of these enhancements can be adjusted based on business needs and feedback.
