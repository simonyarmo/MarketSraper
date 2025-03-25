# MarketSrapper
## Scrapping
There are two web scrappers in this project. A Facebook Marketplace and Ebay scrapper.
#### EBAY Scrapper
For accessablility and simplicity, the ebay scrapper does not use a developers key and can be used by anyone.

**How to Use**

Direct yourself to Scrappers/ebay-scrapper/ebay-srcapper.py

The function ebayScrapper() takes 4 parameters
  - item
  - condition
  - minPrice
  - maxPrice
    
Change the function call on lines 165 in ebay-scrapper.py and run the script.

    if __name__ == "__main__":
    items = ebayScrapper("electronics", "Used",'20','300')

The data sill be collected in Scrappers/ebay-scrapper/ebay-items.json

#### Facebook Scrapper
Since facebook is a private website and has a little more security, scrapping is not as simiple as the Ebay Scrapper. 
*Use at your own risk. Your Facebook accout could be subjected to being banned*

**How to Use**
The facebook scrapper can be called through a Streamlit gui or by simply calling crawl_facebook_marketplace().
##### Set Up
On line 129 replace "FACEBOOK_EMAIL_HERE" with your facebook email and on line 134 replace "FACEBOOK_PASSWORD_HERE" with your facebook password. 

##### Calling the function
To use the scrapper is pretty simple. In lines 239 change the parameters to your specific results. If you want to use a city that is not in the city list, you can add it to the list but ensure you follow the same format as the other cities. 
 
  crawl("Austin", "recents", 1000)
  
  Parameters 
  - City
  - Query
  - maxPrice
##### Using the Gui
To use the gui, in app.py comment out line 239 and uncomment out line 238. Then run the script. This activates the port and has it listen for an event. 

Then go to gui.py. In your terminal cd to Scrapper/Facebook and run streamlit run gui.py. This will open a gui application that will allow you to call the facebook scrapper. 

#### Results

Either way you run the facebook scrapper the results will appear in a json file called facebook.json in your main project folder. 

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

### How to use
- You will need to first get a OPENAI and Perplexity api key
- Once you have your keys, go to the .env file and insert the keys in there proper spot.
- Then go to main.py
- In the "main guard", change the json file you want to be parsed.
- Then click run
- It takes a moment to run through each item in the list
- It then will return in the console items that the agent recommends buying and items not to buy

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






 ### Credit
 Thank you for all of the open source code I used.
  - https://github.com/DannyRivasDev/Ebay-Sold-Listings-Scraper
  - https://github.com/passivebot/facebook-marketplace-scraper



