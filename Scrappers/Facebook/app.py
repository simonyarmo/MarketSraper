# Description: This file contains the code for Passivebot's Facebook Marketplace Scraper API using Selenium.
# Date: 2024-01-24
# Author: Harminder Nijjar (converted to Selenium by You)
# Version: 1.0.0.
# Usage: python app.py

import os
import time
import json
import uvicorn
from fastapi import HTTPException, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup

# Import Selenium dependencies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# Create an instance of the FastAPI class.
app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Define a route to the root endpoint.
@app.get("/")
def root():
    return {"message": "Welcome to Passivebot's Facebook Marketplace API using Selenium. Documentation and additional features are coming soon."}

# Create a route for crawling the Facebook Marketplace
#@app.get("/crawl_facebook_marketplace")
def crawl_facebook_marketplace(city: str, query: str, max_price: int):
    print(f"Starting search for {query} in {city} under ${max_price}")
    # Define dictionary of cities for the Facebook Marketplace URL.
    cities = {
        'New York': 'nyc',
        'Los Angeles': 'la',
        'Las Vegas': 'vegas',
        'Chicago': 'chicago',
        'Houston': 'houston',
        'San Antonio': 'sanantonio',
        'Miami': 'miami',
        'Orlando': 'orlando',
        'San Diego': 'sandiego',
        'Arlington': 'arlington',
        'Balitmore': 'baltimore',
        'Cincinnati': 'cincinnati',
        'Denver': 'denver',
        'Fort Worth': 'fortworth',
        'Jacksonville': 'jacksonville',
        'Memphis': 'memphis',
        'Nashville': 'nashville',
        'Philadelphia': 'philly',
        'Portland': 'portland',
        'San Jose': 'sanjose',
        'Tucson': 'tucson',
        'Atlanta': 'atlanta',
        'Boston': 'boston',
        'Columnbus': 'columbus',
        'Detroit': 'detroit',
        'Honolulu': 'honolulu',
        'Kansas City': 'kansascity',
        'New Orleans': 'neworleans',
        'Phoenix': 'phoenix',
        'Seattle': 'seattle',
        'Washington DC': 'dc',
        'Milwaukee': 'milwaukee',
        'Sacremento': 'sac',
        'Austin': 'austin',
        'Charlotte': 'charlotte',
        'Dallas': 'dallas',
        'El Paso': 'elpaso',
        'Indianapolis': 'indianapolis',
        'Louisville': 'louisville',
        'Minneapolis': 'minneapolis',
        'Oaklahoma City': 'oklahoma',
        'Pittsburgh': 'pittsburgh',
        'San Francisco': 'sanfrancisco',
        'Tampa': 'tampa'
    }

    if city in cities:
        city_code = cities[city]
    else:
        raise HTTPException(404, f'{city.capitalize()} is not currently supported on Facebook Marketplace. Please reach out to us to add this city.')

    # Build the marketplace URL using the city code, query, and max_price.
    marketplace_url = f'https://www.facebook.com/marketplace/{city_code}/search/?query={query}&maxPrice={max_price}'
    initial_url = "https://www.facebook.com/login/device-based/regular/login/"

    # Configure Chrome options (adjust path to chromedriver as needed)
    chrome_options = Options()
    # Set headless to False so you can observe the browser actions; set True to run in headless mode.
    chrome_options.headless = False
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Specify path to your ChromeDriver if not in PATH.
    driver = webdriver.Chrome(options=chrome_options)  # e.g., webdriver.Chrome(executable_path="/path/to/chromedriver", options=chrome_options)
    
    driver.maximize_window()

    # Login process
    driver.get(initial_url)
    time.sleep(2)  # Let the page load
    
    try:
        print("Attempting to login...")
        # Wait for the email input to be present and fill it in.
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "email")))
        email_input = driver.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys("simon.yarmowich@splashbi.com")
        
        # Wait for the password input to be present and fill it in.
        password_input = driver.find_element(By.NAME, "pass")
        password_input.clear()
        password_input.send_keys("Redcar123!")
        
        # Click the login button.
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()
        print("Logged in successfully. Waiting for redirection...")
        time.sleep(5)
    except Exception as e:
        print("Login failed or already logged in:", str(e))
    
    # Navigate to the marketplace URL
    driver.get(marketplace_url)
    print("Navigating to marketplace URL...")
    time.sleep(7)  # Wait for the marketplace page to load

    # Optionally, take a screenshot for debugging
    

    # Retrieve the page source and parse with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    parsed = []
    
    # Adjust the selector below if needed; these classes are based on your current code.
    listings = soup.find_all('div', class_='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24')
    print(f"Found {len(listings)} total listings")
    
    # Parse listings (limit to 100 items as before)
    count = 0
    for listing in listings:
        if count >= 100:
            break
        try:
            #image = listing.find('img', class_='x9f619 x78zum5 x1iyjqo2 x5yr21d x4p5aij x19um543 x1j85h84 x1m6msm x1n2onr6 xh8yej3')['src']
            title = listing.find('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6').text.strip()
            price = listing.find('span', 'x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u').text.strip()
            post_url = listing.find('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xkrqix3 x1sur9pj x1s688f x1lku1pv')['href']
            location = listing.find('span', 'x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xi81zsa').text.strip()
            parsed.append({
                #'image': image,
                'title': title,
                'price': price,
                'post_url': post_url,
                'location': location
            })
            count += 1
            print(f"Successfully parsed item {count}: {title} - {price}")
        except Exception as e:
            print(f"Failed to parse an item: {str(e)}")
            continue

    driver.quit()
    print(f"Finished parsing {len(parsed)} items successfully")

    # Format the results as JSON
    result = []
    for item in parsed:
        result.append({
            'name': item['title'],
            'price': item['price'],
            'location': item['location'],
            'title': item['title'],
            #'image': item['image'],
            'link': item['post_url']
        })
        with open("facebook.json", "w", encoding='utf-8') as file:
            json.dump(result, file, indent=4)
    return result

# Create a route for IP information (unchanged)
@app.get("/return_ip_information")
def return_ip_information():
    # You can keep this using Selenium or any other library if desired.
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.ipburger.com/')
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    ip_address = soup.find('span', id='ipaddress1').text
    country = soup.find('strong', id='country_fullname').text
    location = soup.find('strong', id='location').text
    isp = soup.find('strong', id='isp').text
    hostname = soup.find('strong', id='hostname').text
    ip_type = soup.find('strong', id='ip_type').text
    version = soup.find('strong', id='version').text
    driver.quit()
    return {
        'ip_address': ip_address,
        'country': country,
        'location': location,
        'isp': isp,
        'hostname': hostname,
        'type': ip_type,
        'version': version
    }

def crawl(city, query, max_price):
    return crawl_facebook_marketplace(city, query, max_price)

if __name__ == "__main__":
    # uvicorn.run('app:app', host='127.0.0.1', port=8000)
    crawl("Austin", "recents", 1000)
