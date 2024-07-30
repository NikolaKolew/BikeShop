# BikeShop
This project involves analyzing and documenting data from various CSV files related to sales and product information. The goal is to create a comprehensive data dictionary in Excel, perform data analysis using Python, and generate insights to assist in business decision-making.
## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/NikolaKolew/BikeShop.git
    cd products
    ```

2. Install Dependencies:
- poetry manages dependencies through the pyproject.toml file. Install the required packages using Poetry:

    ```sh
    poetry install
    ```
3. Activate the Virtual Environment:
- Poetry creates a virtual environment for the project. Activate it with:
    ```sh
    poetry shell
    ```

## Files

### Data Dictionary.xlsx
This Excel file contains two sheets:

1. Tables: This sheet provides an overview of each table, including:

- Table Name: The name of the table.
- Description: A brief description of the data contained in the table.
- Total Records: The number of records in the table.
- Data Granularity: The level of detail in the data.
- Business Logic: The business rules or processes that generate the data.
- Business Questions: Potential questions that can be answered using the data in the table.

2. Table Details: This sheet includes detailed information about the columns in each table:

- Table Name: The name of the table.
- Column Name: The name of the column in the table.
- Description: A description of the column's data.
- Primary Key: Indicates whether the column is a primary key.
- Foreign Key: Indicates any foreign key relationships, in the format table_name.column_name.

### Insights.xlsx
Contains the KPIs and insights based on the data analysis. This includes metrics like total sales, number of orders, and performance indicators relevant to the business. These KPIs help in understanding trends and making data-driven decisions.
- Total Sales Revenue: The total amount of money earned from sales.
- Total Number of Orders: The total count of orders placed.
- Average Order Value: The average amount of money spent per order.

## Project Structure
1. Data dictionary
- contains Data_Dictionary.xlsx, Insights.xlsx and create_dictionary.py that creates the Data_Dictionary 
more information with comments can be found in the fail.
2. Source folder with all csv needed for this task product, product_category, sales, etc..
3. load_data.py is reading from the source and populating Data_Dictionary.xlsx
4. report.py is for creating the Insights.xlsx
5. main.py is for all results



