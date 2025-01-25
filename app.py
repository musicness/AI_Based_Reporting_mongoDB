from dotenv import load_dotenv
load_dotenv()  # Load all environment variables
import streamlit as st
import os
from pymongo import MongoClient
import google.generativeai as genai
import json
# Configure the Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and provide SQL query as response
def get_gemini_response(question, prompt):
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-pro')

        # Generate the response
        response = model.generate_content([f"{prompt[0]}\n\n{question}"])

        # Debugging: Print raw response
        # print("\nRaw Response:")
        # print(response)

        # Validate and parse the response
        if hasattr(response, "candidates") and response.candidates:
            # Extract the generated text from the first candidate
            generated_text = response.candidates[0].content.parts[0].text
            
            # Debugging: Print extracted text before cleaning
            # print("\nExtracted Text (before cleaning):")
            # print(generated_text)

            # Clean up the text (remove unnecessary formatting)
            # print(generated_text)
            generated_text = generated_text.strip("```json").strip("```").strip()
            return generated_text
        else:
            # Handle case where response is malformed
            print("Error: Response does not contain 'candidates'.")
            return None
    except AttributeError as e:
        print(f"AttributeError: {e}. Check the response structure.")
        return None
    except KeyError as e:
        print(f"KeyError: {e}. Verify response contains expected keys.")
        return None
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None
# MongoDB connection details
db_name = "vendorData"
collection_name = "vendors"
uri = "mongodb://localhost:27017/"

def read_mongo_query(response):

    try:
        # Connect to MongoDB
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]

        # Execute the query
        results = eval(response) # Evaluate the query string

        return list(results)

    except Exception as e:
        print(f"Error executing MongoDB query: {e}")
        return []

# Define the prompt
prompt = [
    """
        You are an expert in converting English questions to MongoDB queries! 
        The MongoDB database has the name 'vendorData' and a collection named 'vendors'.
        I am using pymongo and want the queries to returned in a way i could use it for wrting in python 
        For example:
            - "show me the list of all the vendors" 
              will be like this: 
              "collection.find({})"
            - "find me the value of the vendor with the highest invoice" 
              will be like this: 
              "collection.find({}, {"invoice_amount": 1, "_id": 0}).sort("invoice_amount", -1).limit(1)" 
              query should be exactly like the above lines.
    """
]

# Streamlit app
st.set_page_config(page_title="Retrieve MongoDB Query", layout="wide")
st.header("Gemini App to Retrieve MongoDB Data")

question = st.text_input("Ask a question:", key="input")
submit = st.button("Generate Query")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    # print(response)
    if response:
        
           d= read_mongo_query(response)
           st.write("Query Result:")
           for x in d:
               st.write(x)
       
    else:
        st.error("Failed to generate MongoDB query.")
