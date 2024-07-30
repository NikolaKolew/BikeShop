import pandas as pd

# Create a new Excel file with two sheets: "Tables" and "Table Details"
with pd.ExcelWriter('Data_Dictionary.xlsx') as writer:
    # Creating empty DataFrames for the required sheets
    tables_df = pd.DataFrame(
        columns=["Table Name", "Description", "Total Records", "Data Granularity", "Business Logic",
                 "Business Questions"])
    table_details_df = pd.DataFrame(columns=["Table Name", "Column Name", "Description", "Primary Key", "Foreign Key"])

    # Writing DataFrames to Excel sheets
    tables_df.to_excel(writer, sheet_name='Tables', index=False)
    table_details_df.to_excel(writer, sheet_name='Table Details', index=False)
