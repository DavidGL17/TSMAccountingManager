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

# Architecture

Currently the app will be a web app using streamlit. The data will be stored in a json file, and the app will be able to read and write to it. The json file will be considered as a database using the `pysonDB` library.
