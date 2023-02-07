# TSMAccountingManager

A Python app to organise, and check all your accounting export from Trade Skill Master in WoW

The idea behind this app is to be able to input the accounting data exported from the TradeSkillMaster desktop app, and to be able to visualize the different gains/losses per categories. This is inspired from Samadans [video](https://www.youtube.com/watch?v=4Na0cF8p91g), but eased up by using python.

I am working on this from time to time so i won't be advancing on it really fast. Contributions is appreciated, even if it is only in the form of advice or remarks!

# Installation

## Requirements

-   Python 3.8
-   Poetry

To install the environment, run the following command in the root of the project:

```bash
poetry install
```

## Usage

Before running, you need to create a config.yml file in the root of the project. This file should contain the contents of the config_example.yml file. You can then edit the file to your needs.

To run the app, run the following command in the root of the project:

```bash
poetry run streamlit run tsmaccountingmanager/main.py
```

# Architecture

Currently the app will be a web app using streamlit. The data will be stored using a ZODB database.

## Frontend

As said above, the frontend will be a web app using streamlit. The idea is to have a simple and easy to use interface. It will be split into different pages to do different things. This part of the app is still in development.

## Backend

The backend will be a python app using ZODB to store the data. The data will be stored in a database, and will be accessible through a series of commands offered by the backend.
