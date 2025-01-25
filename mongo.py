from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["vendorData"]
collection = db["vendors"]

# Clear the collection if it already exists
collection.delete_many({})

# Helper function to generate random data
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Sample data
vendors = ["Vendor A", "Vendor B", "Vendor C", "Vendor D"]

start_date = datetime.now() - timedelta(days=90)  # Start of the last quarter
end_date = datetime.now()

# Insert random data into the collection
records = []
for _ in range(200):
    vendor = random.choice(vendors)
    transaction_date = random_date(start_date, end_date)
    invoice_amount = round(random.uniform(100, 10000), 2)  # Random amount between 100 and 10000

    records.append({
        "vendor": vendor,
        "transaction_date": transaction_date,
        "invoice_amount": invoice_amount
    })

# Insert into MongoDB
collection.insert_many(records)

#close the db connection 
client.close()

print("operation succesfull")
