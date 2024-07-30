import pandas as pd


# Total Sales Revenue: The total amount of money earned from sales.
# Total Number of Orders: The total count of orders placed.
# Average Order Value: The average amount of money spent per order.


sales_df = pd.read_csv("./source_csv_files/sales.csv", delimiter=';')
sales_details_df = pd.read_csv("./source_csv_files/sales_details.csv", delimiter=';')

# Merge sales with sales details to get quantity and unit price information
sales_with_details_df = pd.merge(sales_df, sales_details_df, on="SalesOrderID", how="inner")

# Calculate total sales revenue
sales_with_details_df['total_sales_amount'] = sales_with_details_df['UnitPrice'] * sales_with_details_df['OrderQty']

# Calculate total number of orders
total_orders = sales_df['SalesOrderID'].nunique()

# Calculate total sales revenue
total_sales_revenue = sales_with_details_df['total_sales_amount'].sum()

# Calculate average order value
average_order_value = total_sales_revenue / total_orders if total_orders > 0 else 0

# Create a DataFrame for the KPIs
kpi_data = {
    "KPI": ["Total Sales Revenue", "Total Number of Orders", "Average Order Value"],
    "Value": [total_sales_revenue, total_orders, average_order_value]
}

kpi_df = pd.DataFrame(kpi_data)

with pd.ExcelWriter("./data_dictonary/Insights.xlsx", engine='openpyxl') as writer:
    kpi_df.to_excel(writer, sheet_name='KPIs', index=False)

print("KPIs have been exported to 'Insights.xlsx'.")
