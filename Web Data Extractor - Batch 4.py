# Install required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime as dt
from tqdm import tqdm

main_url = "https://unique.com.mm/collections/mobile-phone"

def create_urls(web_url):
    """Create urls from the main url."""
    
    # Step 1 - Request data from the website  
    ## Get data by using url
    response = requests.get(web_url)
    
    ## Extract html, css, etc.
    web_data = response.text
    
    # Step 2 - Create a beautifulsoup object to read web data
    bsObj = BeautifulSoup(web_data, "html5lib")

    # Step 3 - Extract Last Page Number
    last_page_tag_list = bsObj.find_all("a", "pagination__nav-item link") # tag, class
    last_page_tag = last_page_tag_list[-1]
    last_page_text = last_page_tag.text
    last_page_text = int(last_page_text)

    # Step 4 - Create urls for other web pages
    created_url_list = []
    created_url_list.append(web_url) # insert the default url into url list
    for num in range(2, last_page_text+1):
        new_url = web_url + "?page=" + str(num)
        created_url_list.append(new_url)
    
    print("URL links are created successfully.")
    
    return created_url_list

def get_product_info_tags(url):
    """Extract Product Info Tags and return as a list."""
    
    # Step 1 - Request data from the website
    ## Get data by using url
    response = requests.get(url)

    ## Extract html, css, etc.
    web_data = response.text

    # Step 2 - Create a beautifulsoup object to read web data
    bsObj = BeautifulSoup(web_data, "html5lib")

    # Step 3 - Extract and insert data into the lists
    ## Extract all product info main tags
    product_info_tags_list = bsObj.find_all("div", "product-item__info-inner") # tag, class name
    
    return product_info_tags_list

def create_name_list(product_info_tags_list):
    """Extract product name from the product info tag, and create a product name list."""
    
    name_list = []
    for product_info_tag in product_info_tags_list:
        ## Extract product name tag
        product_name_tag = product_info_tag.find("a", "product-item__title text--strong link") # tag, class name
        ## Extract product name text
        product_name = product_name_tag.text
        name_list.append(product_name)
        
    return name_list

def create_price_list(product_info_tags_list):
    """Extract product price from the product info tag, and create a product price list."""
    price_list = []
    for product_info_tag in product_info_tags_list:
    
        ## Extract product price tag
        product_price_tag = product_info_tag.find("div", "product-item__price-list price-list") # tag, class name
        ## Extract product price text
        product_price = product_price_tag.text
        ## Transform product price
        product_price = product_price.replace(",", "") # remove , from the price text
        product_price = product_price.replace("K", "") # remove K from the price text
        try:
            product_price = int(product_price) # change into int data type
            price_list.append(product_price)
        except ValueError:
            # Handle the discount prices
            discount_price_list = product_price.split("\n")
            # get last value
            product_price = discount_price_list[-1]
            # remove spaces from the text
            product_price = product_price.strip()
            product_price = int(product_price) # change into int data type
            price_list.append(product_price)
    
    return price_list

def create_status_list(product_info_tags_list):
    """Extract product status from the product info tag, and create a product status list."""
    status_list = []
    for product_info_tag in product_info_tags_list:
        ## Extract product status tag
        status_class_list = ["product-item__inventory inventory", "product-item__inventory inventory inventory--high", "product-item__inventory inventory inventory--low"]
        for status_class in status_class_list:
            result = product_info_tag.find("span", status_class)
            if result != None:
                product_status_tag = result
                product_status = product_status_tag.text
                status_list.append(product_status)
    
    return status_list

def get_current_dt():
    """Create current datetime string."""
    # Get Current Date Time
    current_datetime = dt.now()
    # change date to string
    current_datetime = str(current_datetime)
    # replace : with -
    current_datetime = current_datetime.replace(":", "-")
    # remove milliseconds
    current_dt = current_datetime.split(".")[0]
    
    return current_datetime


############################# Main Program #######################################################################

def main():
    """Main program to extract data from the website."""
    ## Step 1 - Create URLs for all web pages
    url_list = create_urls(main_url)

    ## Step 2 - Extract Data From Each URL of the URL List.
    count = 0
    url_count = 0
    final_df = pd.DataFrame() # Create an empty dataframe
    for each_url in tqdm(url_list):
        # Extract product info tags
        p_info_tags_list = get_product_info_tags(each_url)
        
        # Create Product Name List
        p_name_list = create_name_list(p_info_tags_list)
        
        # Create Product Price List
        p_price_list = create_price_list(p_info_tags_list)
        
        # Create Product Status List
        p_status_list = create_status_list(p_info_tags_list)
        
        #print(p_name_list)
        #print(p_price_list)
        #print(p_status_list)
        
        # Create page level dataframe
        page_df = pd.DataFrame({"Product Name":p_name_list,
                           "Price":p_price_list,
                           "Status":p_status_list})
        
        # Get current datetime as string
        current_dt = get_current_dt()
        
        url_count += 1
        # Export as page level excel file
        page_df.to_excel(f"Output_{url_count}_{current_dt}.xlsx", index=False)
        #print(f"Web Page {url_count} is completed successfully!.")
        
        # Export data from all web pages.
        final_df = pd.concat([final_df, page_df])
        
    # Export the final datafraem as an excel file.
    final_df.to_excel(f"All Data_{current_dt}.xlsx", index=False)

    print("Project is completed successfully!")

if __name__ == "__main__":
    main()