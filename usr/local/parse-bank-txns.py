import tabula
import pandas as pd
import os
import traceback

"""
# This script extracts table from PDF files and saves them as csv files and is based on tabula and pandas
# One can easiy ingest csv any reporting tool
# Tested for HDFC bank statements
"""

# Path to PDF bank statement files
pdf_path = "/tmp/Downloads/pdf"

# Path for the output CSV files
output_csv_path = "/tmp/Downloads/csv"

for file in os.listdir(pdf_path):
    pdf_file_path = os.path.join(pdf_path, file)
    csv_file_path = os.path.join(output_csv_path, file.replace('pdf', 'csv'))
    try:
        # Extract tables from all pages of the PDF
        # This returns a list of DataFrames, one for each table found
        print(f"Processing file '{pdf_file_path}'...")
        tables = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True, password="", silent=True)

        if tables:
            extracted_tables = []
            # If multiple tables were extracted, you might want to process each DataFrame
            for i, df in enumerate(tables):
                # Check the columns names in the statement
                if "Txn Date" in df.columns and "Narration" in df.columns:
                    df_1 = df.ffill().fillna(0)
                    # Change the columns names in the statement
                    df_2 = df_1.groupby(['Txn Date','Withdrawals', 'Deposits', 'Closing Balance'])['Narration'].apply(lambda x: ' '.join(str(x))).reset_index()
                    extracted_tables.append(df_2)
            final_dataframe = pd.concat(extracted_tables, ignore_index=True)
            final_dataframe.to_csv(csv_file_path, index=False)
            print(f"Successfully converted '{pdf_file_path}' to '{csv_file_path}'.")
        else:
            print(f"No tables found in '{pdf_file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())