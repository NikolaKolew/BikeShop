import pandas as pd
import os

# List of CSV files to import
csv_files = ["product.csv", "special_offer.csv", "product_category.csv", "product_subcategory.csv", "sales.csv",
             "sales_details.csv"]

# Dictionary to hold DataFrames
dataframes = {}

# Import each CSV file
for file in csv_files:
    table_name = os.path.splitext(file)[0]  # Get the table name without the file extension
    df = pd.read_csv(f'./source_csv_files/{file}',  on_bad_lines='skip', delimiter=';')
    dataframes[table_name] = df

# Displaying the first few rows of each table to understand the data
for table_name, df in dataframes.items():
    print(f"Table: {table_name}")
    print(df.head(), "\n")


tables_data = [
    {
        "Table Name": "product",
        "Description": "Contains product details such as name, category, and price.",
        "Total Records": len(dataframes["product"]),
        "Data Granularity": "Each row represents a single product.",
        "Business Logic": "Data is created when new products are added to the inventory.",
        "Business Questions": "What are the best-selling products? What is the average price of products?"
    },
    {
        "Table Name": "special_offer",
        "Description": "Contains product discount details it contains columns like Category, Type, StartDate and EndDate.",
        "Total Records": len(dataframes["special_offer"]),
        "Data Granularity": "Each row represents a single offer.",
        "Business Logic": "Data is created for specific discount for specific product.",
        "Business Questions": "How much the sales are increased with the offers "
    },
    {
        "Table Name": "product_category",
        "Description": "Contains product categories such as Bikes, Components, Clothing, Accessories",
        "Total Records": len(dataframes["product_category"]),
        "Data Granularity": "Each row represents a single category.",
        "Business Logic": "Data is created to separate the products by categories.",
        "Business Questions": "Which is the most popular category"
    },
    {
        "Table Name": "product_subcategory",
        "Description": "Contains subcategories for product_categories table, contains different bike and parts categories",
        "Total Records": len(dataframes["product_subcategory"]),
        "Data Granularity": "Each row represents a single subcategory.",
        "Business Logic": "Data is created to separate the categories by subcategories.",
        "Business Questions": "Which is the most popular subcategory for bikes"
    },
    {
        "Table Name": "sales",
        "Description": "Contains sales information and details like SalesOrderID, OrderDate and etc.",
        "Total Records": len(dataframes["sales"]),
        "Data Granularity": "Each row represents a order.",
        "Business Logic": "Data is created to keep track of the sales.",
        "Business Questions": "How fast is the delivery of the orders"
    },
    {
        "Table Name": "sales_details",
        "Description": "Contains details about the sales and information like if there is a specific sales offer, tracking number etc.",
        "Total Records": len(dataframes["sales_details"]),
        "Data Granularity": "Each row represents a details for specific order.",
        "Business Logic": "Data is created to keep track of the sales details.",
        "Business Questions": "How many orders are made with discount"
    },

]

# Convert to DataFrame and append to "Tables" sheet
tables_df = pd.DataFrame(tables_data)
with pd.ExcelWriter('./data_dictonary/Data_Dictionary.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    tables_df.to_excel(writer, sheet_name='Tables', index=False)


table_details_data = []
for table_name, df in dataframes.items():
    for column in df.columns:
        table_details_data.append({
            "Table Name": table_name,
            "Column Name": column,
            "Description": "",
            "Primary Key": "Yes" if "id" in column.lower() else "No",
            "Foreign Key": ""
        })

# Convert to DataFrame and append to "Table Details" sheet
table_details_df = pd.DataFrame(table_details_data)
with pd.ExcelWriter('./data_dictonary/Data_Dictionary.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    table_details_df.to_excel(writer, sheet_name='Table Details', index=False)
