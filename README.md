# MarketSrapper
MarketScraper is an AI-powered resale opportunity finder that helps you identify profitable items to flip by analyzing current listings and comparing them to historical sales data.

## Scrapping
There are two web scrapers in this project. A Facebook Marketplace and Ebay scraper.
#### EBAY Scraper
For accessablility and simplicity, the ebay scraper does not use a developers key and can be used by anyone.

**How to Use**

Direct yourself to Scrapers/ebay-scraper/ebay-srcapper.py

The function ebayScraper() takes 4 parameters
  - item
  - condition
  - minPrice
  - maxPrice
    
Change the function call on lines 165 in ebay-scraper.py and run the script.

    if __name__ == "__main__":
    items = ebayScraper("electronics", "Used",'20','300')

The data sill be collected in Scrapers/ebay-scraper/ebay-items.json

#### Facebook Scraper
Since facebook is a private website and has a little more security, scrapping is not as simiple as the Ebay Scraper. 
*Use at your own risk. Your Facebook accout could be subjected to being banned*

**How to Use**
The facebook scraper can be called through a Streamlit gui or by simply calling crawl_facebook_marketplace().
##### Set Up
On line 129 replace "FACEBOOK_EMAIL_HERE" with your facebook email and on line 134 replace "FACEBOOK_PASSWORD_HERE" with your facebook password. 

##### Calling the function
To use the scraper is pretty simple. In lines 239 change the parameters to your specific results. If you want to use a city that is not in the city list, you can add it to the list but ensure you follow the same format as the other cities. 
 
  crawl("Austin", "recents", 1000)
  
  Parameters 
  - City
  - Query
  - maxPrice
##### Using the Gui
To use the gui, in app.py comment out line 239 and uncomment out line 238. Then run the script. This activates the port and has it listen for an event. 

Then go to gui.py. In your terminal cd to Scraper/Facebook and run streamlit run gui.py. This will open a gui application that will allow you to call the facebook scraper. 

#### Results

Either way you run the facebook scraper the results will appear in a json file called facebook.json in your main project folder. 

#### When Runing the program

Facebook is a very secure website and does not like having bots scrap its website for data. If you try to run this program, chances are it will not be successful due to facebooks aint bot features. To get around this you need to step through the function.
Steps
- Add a break point at line 140, after the program opens a headless chrome browser and logs you into facebook.
- Typically a MyCapcha will appear asking you to prove you are not a bot.
- You will need to fill this out manually.
- Once completed you can contiune the program.
- It will redirect you to facebook market place and scrap all of the items that have loaded
- If you want more items. Add another break point on line 145, after it has directed you to facebook market place.
- Scroll down on the website and load as many items as you want
- Resume the program


## AI AGENT

## ✨ Features

- 🔍 **Real-Time Web Search** using Perplexity or custom scraping tools
- 💰 **Price vs. Sold Comparison** using recent eBay listings
- 🧠 **AI-Powered Recommendations** on whether or not to buy
- 📊 **Profit Margin Estimator** (e.g., 15% threshold)
- 📁 Supports JSON data input from Facebook Marketplace, Craigslist, etc.

## 🚀 Quick Start

### 1. Clone the repo
### 2. Set up your environment
Create a `.env` file:
```env
OPENAPI_KEY=your_openai_key
PERPLEXITY_KEY=your_perplexity_key
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the agent
```bash
python main.py

 ### How it works
 - Run calls a function in the Agent folder called find_best_deals(items). Items is a list of the items from the json folder
 - Find_best_deals() calls the main_agent() function. This contains my controller agent.
 - In main_agent(), the model is given each item that needs to processed. The model has access to a tool called decision_agent(item, price).
 - For each item the main agent calls decision_agent(item,price). Decision_agent returns whether or not the item should be purchased.
 - Decision_agent has two tools search_for_item() and ebay_recently_sold().
 - search_for_item() uses perplexities api and websearch capabilities to look through the web for recently sold items. If it is a branded item, it focuses on finding the retail price off of the brand's website. Otherwise it looks for recently sold items.
 - ebay_recently_sold() uses BeautifulSoup to parse ebays html script to find recently sold items on ebay.
 - decision_agent then uses the results from its two tools to decide whether or not an item is worth buying.
 - An item is worth buying if
 -          - If the margin of profit is greater than 15% then you should recommend buying.
            - If the item is at least 5% cheaper than the average price of similar items, recommend buying.
            - If the item is in good condition and the price is reasonable, recommend buying.
            - If the item's price is 10% less than the brand new price.
 - The results from decision_agent is then collected in the main agent and main agent returns a list of recommended items to buy and items to not buy.
 - The results are stored in 4 arrays, recommended = list of items to buy, recommend_reasons = reason why to buy, dont_buy = list of items not to buy, dont_buy_reasons = list of reasons why not to buy.
 - Each array is printed to the console.
```
## Credit
 Thank you for all of the open source code I used.
  - https://github.com/DannyRivasDev/Ebay-Sold-Listings-Scraper
  - https://github.com/passivebot/facebook-marketplace-scraper

Also thank you to Steven Morrisroe for the idea



