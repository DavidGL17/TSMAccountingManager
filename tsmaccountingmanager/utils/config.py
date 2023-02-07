import yaml

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

timezone = config["timezone"]
db_folder = config["db_folder"]
logging_level = config["logging_level"]
log_file = config["log_file"]
