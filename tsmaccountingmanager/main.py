"""The main module of the application.

"""

import streamlit as st


DATE_COLUMN = "date/time"
DATA_URL = "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"


def main():
    """The main function of the application."""
    st.title("TSM Accounting Manager")


if __name__ == "__main__":
    main()
