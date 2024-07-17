from bs4 import BeautifulSoup
import requests
import re
import csv

def finding_number_of_pages(doc):
    page_span = doc.find("span", class_="list-tool-pagination-text")
    page_element = page_span.find("strong")
    num_of_pages = int(page_element.text.split("/")[1])
    return num_of_pages

def extract_price(price_div):
    price_current = price_div.ul.find(class_="price-current")
    strong = price_current.find("strong")
    sup = price_current.find("sup")
    if strong and sup:
        item_price = float(strong.string.replace(",","")) + float (sup.string)
        return item_price
    elif strong:
        item_price = float(strong.string.replace(",","")) 
        return item_price
    elif sup:
        item_price = float (sup.string)
        return item_price
    else:
        return None
    
def export_data(product_name,items_found):
    # Define the CSV file name
    csv_file = f"{product_name}_products.csv"

    # Write the scraped data to the CSV file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["title", "price", "link"])
        writer.writeheader()
        writer.writerows(items_found)

    print("Data exported to:", csv_file)

def main():
    product_name = input("What product do you want to search for? ")
    #product_name = "keyboard"
    
    url = f"https://www.newegg.ca/p/pl?d={product_name}&N=4131"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    # Finding the number of pages
    num_of_pages = finding_number_of_pages(doc)

    items_found = []

    print(f"Number of Pages :  {num_of_pages}")

    for page in range(1, num_of_pages + 1):
        url = f"https://www.newegg.ca/p/pl?d={product_name}&N=4131&page={page}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        items_div = doc.find(class_="item-cells-wrap border-cells short-video-box items-grid-view four-cells expulsion-one-cell")
        items = items_div.find_all('div',recursive=False)

        for item in items:
            item = item.find('div')

            #Link
            item_link_element = item.find('a',{'class':'item-img'})
            item_link = item_link_element.get("href")
            
            # Title
            item_info_div = item.find('div', {'class': 'item-info'})
            item_title = None
            title_element = item_info_div.find('a', {'class': 'item-title'}) if item_info_div else None
            if title_element:
                item_title = title_element.text

            # Extracting price
            price_div = item.find(class_="item-action")
            item_price = extract_price(price_div)
            
            items_found.append({
                "title": item_title,
                "price": item_price,
                "link": item_link
            })
    
    export_data(product_name , items_found)

if __name__ == "__main__":
    main()