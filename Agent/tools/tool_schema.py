tools = [
    {
        "type": "function",
        "function": {
            "name": "search_for_item",
            "description": "Search for an item on the internet. Returns the title, description, price, and website link of the top choices.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "item e.g. iPhone 13 pro"
                    }
                },
                "required": [
                    "item"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ebay_recently_sold",
            "description": "Search for a recently sold item on ebay. Returns an array of recently sold items.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Item e.g. iPhone 13 pro"
                    }
                },
                "required": [
                    "item"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]
