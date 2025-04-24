import os
import yaml 
import pandas as pd
from src.logger import get_logger

logger = get_logger(__name__)

def load_data(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"error in loading data")
        return("failed to load data")

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File does not exist")
        with open(file_path,"r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            return config
    except Exception as e:
        logger.error("error reading yaml file")

