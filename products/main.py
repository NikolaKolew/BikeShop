import pandas as pd
import os


def main():
    csv_files = ["product.csv", "special_offer.csv", "product_category.csv", "product_subcategory.csv", "sales.csv",
                 "sales_details.csv"]
    dataframes = {}
    result = []

    # returns the product names and total sold quantity in descending order of quantity sold
    for file in csv_files:
        table_name = os.path.splitext(file)[0]  # Get the table name without the file extension
        df = pd.read_csv(f'./source_csv_files/{file}', on_bad_lines='skip', delimiter=';')
        dataframes[table_name] = df

    sales_df = dataframes["sales"]
    sales_details_df = dataframes["sales_details"]
    special_offer_df = dataframes["special_offer"]
    product_df = dataframes["product"]
    product_category_df = dataframes["product_category"]
    product_subcategory_df = dataframes["product_subcategory"]


    merged_sales_df = sales_details_df.merge(sales_df, on="SalesOrderID").merge(product_df, on="ProductID")
    product_sales = merged_sales_df.groupby("Name")["OrderQty"].sum().reset_index().sort_values(by="OrderQty",
                                                                                                  ascending=False)

    merged_sales_df['OrderDate'] = pd.to_datetime(merged_sales_df['OrderDate'])
    special_offer_df['StartDate'] = pd.to_datetime(special_offer_df['StartDate'])
    special_offer_df['EndDate'] = pd.to_datetime(special_offer_df['EndDate'])

    # returns the name and number of orders of each product when the product was on sale
    for _, offer in special_offer_df.iterrows():
        start_date = offer['StartDate']
        end_date = offer['EndDate']

        # Filter sales that are within the special offer period
        on_sale_df = merged_sales_df[
            (merged_sales_df['OrderDate'] >= start_date) &
            (merged_sales_df['OrderDate'] <= end_date)
            ]

        # Group by product and count the number of orders
        sales_count = on_sale_df.groupby('ProductID').size().reset_index(name='NumberOfOrders')

        # Merge with product details to get product names
        sales_count = pd.merge(sales_count, product_df[['ProductID', 'Name']], on='ProductID', how='left')

        # Append results
        result.append(sales_count)

    # Combine all results
    final_result_df = pd.concat(result).groupby('ProductID').agg({
        'Name': 'first',
        'NumberOfOrders': 'sum'
    }).reset_index()

    # Find the product with the highest number of orders
    most_sales_product = final_result_df.loc[final_result_df['NumberOfOrders'].idxmax()]



    sales_details_df['UnitPriceDiscount'] = sales_details_df['UnitPriceDiscount'] / 100.0

    # Calculate unit discount
    sales_details_df['unit_discount'] = sales_details_df['UnitPrice'] * sales_details_df['UnitPriceDiscount']

    # Calculate total discount
    sales_details_df['total_discount'] = sales_details_df['unit_discount'] * sales_details_df['OrderQty']

    # Calculate original price and discounted price
    sales_details_df['original_price'] = sales_details_df['UnitPrice'] * sales_details_df['OrderQty']
    sales_details_df['discounted_price'] = sales_details_df['original_price'] - sales_details_df['total_discount']

    print("Updated Sales Details DataFrame with Discounts:")
    print(sales_details_df[
              ['SalesOrderID', 'SalesOrderDetailID', 'CarrierTrackingNumber', 'OrderQty', 'ProductID', 'SpecialOfferID',
               'UnitPrice', 'UnitPriceDiscount', 'LineTotal', 'rowguid', 'ModifiedDate',
               'unit_discount', 'total_discount']])

    sales_details_df.to_csv("updated_sales_details.csv", index=False)

    # Count the number of orders per customer
    order_counts = sales_df['CustomerID'].value_counts()

    # Determine the maximum number of orders
    max_orders = order_counts.max()

    # Find all customer IDs with the maximum number of orders
    top_customers = order_counts[order_counts == max_orders].index.tolist()

    sales_with_category_df = pd.merge(merged_sales_df, product_subcategory_df, on="ProductSubcategoryID", suffixes=('rowguid_x', 'ModifiedDate_x')).merge(
        product_category_df, on="ProductCategoryID", how="inner")

    # Calculate total sales amount and total discounted amount
    sales_with_category_df['total_sales_amount'] = sales_with_category_df['UnitPrice'] * sales_with_category_df[
        'OrderQty']
    sales_with_category_df['total_discounted_amount'] = sales_with_category_df['UnitPrice'] * sales_with_category_df[
        'OrderQty'] * sales_with_category_df['UnitPriceDiscount'] / 100.0

    # Group by category to get total sales amount, total discounted amount, and total number of orders
    category_summary_df = sales_with_category_df.groupby('Name').agg(
        total_sales_amount=('total_sales_amount', 'sum'),
        total_discounted_amount=('total_discounted_amount', 'sum'),
        total_orders=('SalesOrderID', 'nunique')
    ).reset_index()

    # Find the category with the highest sales amount
    highest_sales_category = category_summary_df.loc[category_summary_df['total_sales_amount'].idxmax()]

    # Find the category with the highest number of orders
    highest_orders_category = category_summary_df.loc[category_summary_df['total_orders'].idxmax()]

    # Results
    print("Category Summary:")
    print(category_summary_df)
    print("\nCategory with the Highest Sales Amount:")
    print(highest_sales_category)
    print("\nCategory with the Highest Number of Orders:")
    print(highest_orders_category)

    print(f"Customer(s) with the most orders ({max_orders} orders):")
    print(top_customers)

    print("Product Sales During Special Offers:")
    print(final_result_df)
    print("\nProduct with the Highest Number of Sales During Special Offers:")
    print(most_sales_product)

    print("Product with highest quantity sold:", product_sales.iloc[0])
    print("Product with lowest quantity sold:", product_sales.iloc[-1])
    print(product_sales)


if __name__ == "__main__":
    main()

# RESULTS

#  result of checking the order with highest and lowest sold quantity
# Name                              OrderQty
#
# AWC Logo Cap                        8311
#
# LL Touring Frame - Blue, 58         4

# Product with the Highest Number of Sales During Special Offers:
# ProductID                           870
# Name              Water Bottle - 30 oz.
# NumberOfOrders                    31233

# Customer(s) with the most orders (28 orders): ID: 11091 and 11176

# Category with the Highest Sales Amount:
# Name                               Bikes
# total_sales_amount         95145813.3519
# total_discounted_amount      4946.406472
# total_orders                       18368

# Category with the Highest Number of Orders:
# Name                        Accessories
# total_sales_amount         1278760.9125
# total_discounted_amount       66.880286
# total_orders                      19524