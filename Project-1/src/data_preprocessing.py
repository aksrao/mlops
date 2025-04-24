import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from utils.common_functions import read_yaml,load_data

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self,train_path,test_path,processed_dir,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config_path = config_path


    def Preprocess_data(self,df):
        try:
            df.drop(columns=["unnamed:0", "Booking_ID"], inplace=True)
            df.drop_duplicates(inplace=True)



        expect: