"""The main module of the application.

"""

import streamlit as st
from tsmaccountingmanager.utils.logger import logger


def main():
    """The main function of the application."""
    st.title("TSM Accounting Manager")


if __name__ == "__main__":
    logger.info("Starting application...")
    main()
