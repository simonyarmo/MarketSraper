import json
from Agent import agent

def getItems(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = []
    for entry in data:
        item_str = ",\n        ".join([f"{key}: {value}" for key, value in entry.items()])
        items.append(item_str)

    return items

def run():
    print("Finding the snags...")
    # Get the items from the file
    items = getItems("facebook.json")
    
    # Get categorized results
    results = agent.find_best_deals(items)
    
    # Print the results in a formatted way
    print("\nRecommended Purchases:")
    for i in range(len(results["recommended"])):
        print(results["recommended"][i])
        print(results["recommended_reasons"][i]+"\n")
    print("\nItems to Avoid:")
    for i in range(len(results["dont_buy"])):
        print(results["dont_buy"][i])
        print(results["dont_buy_reasons"][i]+"\n")


if __name__ == "__main__":
    run()