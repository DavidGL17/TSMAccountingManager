"""
A streamlit page to import data from a csv file.
"""
from tsmaccountingmanager.backend.data_handler import process_expenses, process_sales

import streamlit as st
import pandas as pd


st.title("Import data")
st.write(
    "Import data from a csv file. To obtain the csv file, you need to use TSM's desktop app. Since the csv files between expenses and sales are the same format, you need to be careful to import the correct file in the correct section."
)

st.subheader("Import expenses")
expenses_file = st.file_uploader("Add your expenses csv file", type="csv")

st.subheader("Import sales")
sales_file = st.file_uploader("Add your sales csv file", type="csv")

# Add button to process data
if st.button("Import data"):
    if expenses_file is not None:
        expenses = pd.read_csv(expenses_file)
        result_expenses, ctr_expenses = process_expenses(expenses)
        # Show a text to the user with the number of expenses added to the database
        st.write(f"Added {ctr_expenses} new expenses to the database.")
        # then reset the file uploader
        expenses_file = None
    else:
        st.write("No expenses file uploaded")
    if sales_file is not None:
        sales = pd.read_csv(sales_file)
        result_sales, ctr_sales = process_sales(sales)
        # Show a text to the user with the number of sales added to the database
        st.write(f"Added {ctr_sales} new sales to the database.")
        # then reset the file uploader
        sales_file = None
    else:
        st.write("No sales file uploaded")
