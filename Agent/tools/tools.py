import requests
from openai import OpenAI
import dotenv
import os
import json
from bs4 import BeautifulSoup
import requests
from .tool_schema import tools
dotenv.load_dotenv()

def search_for_item(item):
    api_keys = os.getenv("PERPLEXITY_KEY")
    client = OpenAI(api_key=api_keys, base_url="https://api.perplexity.ai")
    messages= [
            {
                "role": "system",
                "content": """You are an AI assistant that performs real-time web search.
                Find at least 5 recent items matching the user's query. For each item, return:
                - title
                - short description
                - price
                - website link
                Format your answer as a list of lists: [title, description, price, website].
                Search for items that are on a resale websites first like ebay, craigslist, or facebook marketplace.
                If the item is part of a brand like, Lulu Lemon, Macys, Apple, ect, search for the item on the brand's website.
                Return the items in the following format:
                {[title, description, price, website],[title,description,price,website]...}
                """
            
            },
            {
                "role": "user",
                "content": f"Find listings for: {item}"
            }
        ]

    response = client.chat.completions.create(
        model="sonar",
        messages=messages,
    )
    data = response.choices[0].message.content
    print(data)


def ebay_recently_sold(item):
    search_item = item
    search_item = search_item.split(" ")
    search_item = ("+").join(search_item)

    # Example item: nintendo switch oled
    items_list = []
    f = open("Sold_listings.txt", "w")
    # The range of pages starting at page 1
    for i in range(3)[1:]:
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_item}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn={i}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        page = doc.find(class_="srp-results srp-list clearfix")

        listings = page.find_all("li", class_="s-item s-item__pl-on-bottom")

        for item in listings:
            title = item.find(class_ = "s-item__title").text
            price = item.find(class_ = "s-item__price").text
            date = item.find(class_ = "POSITIVE").string
            link = item.find(class_ = "s-item__link")['href'].split("?")[0]
            
            f.write(f"Title: {title}\n")
            f.write(f"Price: {price}\n")
            f.write(f"Date: {date}\n")
            f.write(f"Link: {link}\n")
            f.write("---\n")

            if price != None:
                price = price.replace("$", "")
                price = price.replace(",", "")
                if 'to' in price:
                    price = sum([float(num) for num in price.split() if num != 'to']) / 2
                    price = round(price, 2)
                else:
                    price = float(price)
                if price < 500:
                    items_list.append({
                        "title": title,
                        "price": price,
                        "date": date,
                        "link": link
                    })

    f.close()
    return items_list

available_functions = {
    "search_for_item": search_for_item,
    "ebay_recently_sold": ebay_recently_sold
}


def decision_agent(item,price):
    client = OpenAI(api_key=os.getenv("OPENAPI_KEY"))
    # Create a working copy of messages
    message = [
    {
        "role": "system",
        "content": """You are a helpful assistant with access to the following tools:
        - search_for_item: Searches the web for items and returns a list of recently sold items.
        - ebay_recently_sold: Searches eBay for recently sold items.

        When using a tool responde with <function>tool_name </function> content</function>.
        Your job is to determine wether or not an item is worth buying. 
        **Use both tools to find the price of the item and what it sold for**
        You will use your tools to find the price of similar items and what they sold for.
        **Whats worth buying?**
            - If the margin of profit is greater than 15% then you should recommend buying.
            - If the item is at least 5% cheaper than the average price of similar items, recommend buying.
            - If the item is in good condition and the price is reasonable, recommend buying.
            - If the item's price is 10% less than the brand new price.        
        For general questions and responses, respond directly without using any tools.
        """
    },
    {"role": "user", "content": "Item: "+item+ "Price: "+ price}
]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message,
        tools=tools
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        # Add the assistant's message to the conversation
        message.append({
            "role": "assistant",
            "content": msg.content if msg.content else None,
            "tool_calls": [tool_call.model_dump() for tool_call in msg.tool_calls]
        })

        for tool_call in msg.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"[Tool Requested] {function_name}({arguments})")

            # Call the function and get the response
            function_response = available_functions[function_name](**arguments)

            # Add the tool response to the conversation
            message.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(function_response)
            })

        # Get the final response using the updated conversation
        final_response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=message,
            tools=tools
        )

        print("[Assistant Final Response]")
        print(final_response.choices[0].message.content)
        return final_response.choices[0].message.content

    else:
        # No tool call — just print regular message
        print("[Assistant]")
        print(msg.content)
        return msg.content



