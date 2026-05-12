# web-scraping-project-batch4
Final Capstone Project

## Unique Mobile Scraper

A Python-based web scraping tool designed to extract mobile phone product information from **unique.com.mm**. The script crawls through multiple pagination pages, extracts key product details, and exports the data into organized Excel files.

---

### ## Features

* **Automatic Pagination:** Automatically detects the total number of pages and generates the necessary URLs.
* **Data Extraction:** Collects Product Names, Prices (cleaned and formatted as integers), and Inventory Status.
* **Robust Cleaning:** Handles complex price strings (removing currency symbols and commas) and manages discounted price variations.
* **Multi-format Export:**
* Saves individual Excel files for every page scraped.
* Generates a master "All Data" Excel file combining all results.


* **Progress Tracking:** Uses `tqdm` to provide a real-time progress bar in the console.

---

### ## Prerequisites

Before running the script, ensure you have Python installed and the following libraries:

```bash
pip install requests beautifulsoup4 pandas tqdm html5lib openpyxl

```

---

### ## Project Structure

* `main_url`: The starting point for the scraper (Mobile Phone collection).
* `create_urls()`: Navigates the pagination to build a list of all sub-pages.
* `get_product_info_tags()`: Parses the HTML to isolate product information containers.
* `create_name_list()`, `create_price_list()`, `create_status_list()`: Modular functions for extracting and cleaning specific data points.
* `main()`: Orchestrates the workflow, handles data concatenation, and manages file exports.

---

### ## How To Use

1. **Clone or Copy** the script to your local machine.
2. **Open your terminal** or command prompt in the project folder.
3. **Run the script**:
```bash
python your_script_name.py

```


4. **Check Output:** The script will generate `.xlsx` files in the same directory. Each file is timestamped with the current date and time to prevent overwriting.

---

### ## Data Schema

The exported Excel files contain the following columns:

| Column Name | Description |
| --- | --- |
| **Product Name** | Full name of the mobile device. |
| **Price** | Numerical price (MMK) formatted as an integer. |
| **Status** | Current availability (e.g., In stock, Low stock). |

---

### ## Important Note

> [!WARNING]
> **Web Scraping Ethics:** This tool is for educational purposes. Ensure you comply with the website's `robots.txt` policy and terms of service. Do not overwhelm the server with excessive requests.

```

```
