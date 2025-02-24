import requests
import json
from bs4 import BeautifulSoup
  
API_KEY = "91e44c53067ed863391ef9ad387fa688"
url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1312&_nkw=airpods+pro&_sacat=0"
  
payload = {"api_key": API_KEY, "url": url}
r = requests.get("http://api.scraperapi.com", params=payload)
html_response = r.text
soup = BeautifulSoup(html_response, "lxml")
  
  
result_list = []
  
# Find all product items on the page
listings = soup.find_all("div", class_="s-item__info clearfix")
images = soup.find_all("div", class_="s-item__wrapper clearfix")
  
for listing, image_container in zip(listings, images):
    title = listing.find("div", class_="s-item__title").text
    price = listing.find("span", class_="s-item__price").text
  
    product_url = listing.find("a")
    link = product_url["href"]
  
    product_status_element = listing.find("div", class_="s-item__subtitle")
    product_status = (
        product_status_element.text
        if product_status_element is not None
        else "No status available"
    )
  
    if title and price:
        title_text = title.strip()
        price_text = price.strip()
        status = product_status.strip()
  
        image = image_container.find("img")
        image_url = image["src"]
  
        result_dict = {
            "title": title_text,
            "price": price_text,
            "image_url": image_url,
            "status": status,
            "link": link,
        }
        result_list.append(result_dict)
  
# print(result_list)
  
# Output the result in JSON format
output_json = json.dumps(result_list, indent=2)
  
# Write the JSON data to a file
with open("ebay_results.json", "w", encoding="utf-8") as json_file:
    json_file.write(output_json)
  
print("JSON data has been written to ebay_results.json")