from openai import OpenAI
import dotenv
import os
from Agent.tools.tools import decision_agent
import json
import re

dotenv.load_dotenv()

available_functions = {
    "decision_agent": decision_agent
}
tools =[{
        "type": "function",
        "function": {
            "name": "decision_agent",
            "description": "Decides whether an item is worth it to buy based on the price and what it has previously sold for. Decision_agent uses two tools, search_for_item and ebay_recently_sold, to find the price of the item and what it sold for. If the margin of profit is greater than 15% then you should recommend buying.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Item e.g. iPhone 13 pro"
                    },
                    "price": {
                        "type": "string",
                        "description": "Price of the item being sold"
                    }
                },
                "required": [
                    "item",
                    "price"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
        }]


def main_agent(item_list):
    client = OpenAI(api_key=os.getenv("OPENAPI_KEY"))
    message = [
    {
        "role": "system",
        "content": """You are a helpful assistant. Your purpose is to return items that I should buy. You have access to the following tools:
        - decision_agent: Decides whether an item is worth it to buy based on the price and what it has previously sold for. Decision_agent uses two tools, search_for_item and ebay_recently_sold, to find the price of the item and what it sold for. If the margin of profit is greater than 15% then you should recommend buying.
        When using a tool responde with <function>tool_name </function> content</function>.
        **You should use decision_agent to determine if an item is worth buying for every item.**
        For general questions and responses, respond directly without using any tools.
        For each item return whether I should buy it or not and a reason why.
        Format: <Item>Item</Items><recommendation>recommend buying</recommendation><reason>Reason</reason>
        """
    }
    ]
    # Create a working copy of messages
    for item in item_list:
        message.append({
            "role": "user",
            "content": item
        })
    
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
    


def find_best_deals(item_list):
    recommended_items = []
    recommended_items_reasons = []
    dont_buy = []
    dont_buy_reasons = []

    # Run the agent once for the full list
    response = main_agent(item_list)

    # Find all item blocks using regex
    pattern = r"<Item>(.*?)</Item><recommendation>(.*?)</recommendation><reason>(.*?)</reason>"
    matches = re.findall(pattern, response, re.DOTALL)

    for item, recommendation, reason in matches:
        item = item.strip()
        recommendation = recommendation.strip().lower()
        reason = reason.strip()

        if "recommend buying" in recommendation:
            recommended_items.append(item)
            recommended_items_reasons.append(reason)
        else:
            dont_buy.append(item)
            dont_buy_reasons.append(reason)

    return {
        "recommended": recommended_items,
        "recommended_reasons": recommended_items_reasons,
        "dont_buy": dont_buy,
        "dont_buy_reasons": dont_buy_reasons
    }

if __name__ == "__main__":
    item_list = ["8ft Pool table, good condition, Price: 200", "iPhone 13 pro, Price: 100", "2021 Macbook pro 256GB, Price: 500"]
    # Process each item individually
    for item in item_list:
        main_agent(item)
