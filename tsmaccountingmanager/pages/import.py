"""
A streamlit page to import data from a csv file.
"""
from tsmaccountingmanager.backend.data_handler import process_expenses, process_sales

import streamlit as st
import pandas as pd


"""
A streamlit page to import data from a csv file.
"""
st.title("Import data")
st.write("Import data from a csv file.")

st.subheader("Import expenses")
expenses_file = st.file_uploader("Add your expenses csv file", type="csv")

st.subheader("Import sales")
sales_file = st.file_uploader("Add your sales csv file", type="csv")

# Add button to process data
if st.button("Import data"):
    if expenses_file is not None:
        expenses = pd.read_csv(expenses_file)
        process_expenses(expenses)
    if sales_file is not None:
        sales = pd.read_csv(sales_file)
        process_sales(sales)
