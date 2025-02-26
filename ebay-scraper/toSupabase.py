import mysql.connector
from supabase import create_client, Client
from langchain_openai import OpenAIEmbeddings
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check if environment variables are set
if not SUPABASE_KEY:
    raise ValueError("The SUPABASE_KEY environment variable is not set.")
if not SUPABASE_URL:
    raise ValueError("The SUPABASE_URL environment variable is not set.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

key = os.getenv("OPENAPI_KEY")
embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=key)

def upload_to_supabase(content, metadata, price, link, url, databaseName):
    try:
        embedding_vector = embeddings_model.embed_query(content)

        data = {
            "content": content,
            "metadata": json.loads(metadata),  
            "embedding": embedding_vector,
            "price": price,
            "link": link,
            "image_url":url 
        }
        response = supabase.table(databaseName).insert(data).execute()
        
        if hasattr(response, "data") and response.data:  
            print("Data successfully uploaded to Supabase.")
        else:
            print(f"⚠️ Upload may have failed. Response: {response}")

    except Exception as e:
        print(f"Error uploading to Supabase: {e}")

if __name__ == "__main__":
    with open("data.json","r") as file:
        items_data = json.load(file)
    for item in items_data:
        table ={
            "content": item["Title"],
            "metadata": json.dumps({"joins": item})
        }

        upload_to_supabase(table['content'],table['metadata'], item['Price'], item['Link'],item['Image Link'],"documents")
