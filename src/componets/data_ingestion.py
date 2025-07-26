import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.componets.data_transformation import DataTransformation, DataTransformationConfig

@dataclass  #use this decorator only if variables inside the class
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv') # add artifacts folder into gitignore
    test_data_path: str = os.path.join('artifacts', 'test.csv') # add artifacts folder into gitignore
    raw_data_path: str = os.path.join('artifacts', 'raw.csv') # add artifacts folder into gitignore


class DataIngestion:
    def __init__(self):  # use __init__ if functions inside the class
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion method started")
        try:
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info("Dataset read as pandas DataFrame")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw data saved")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Train and Test data saved")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
                # self.ingestion_config.raw_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)
        

if __name__ == "__main__":
    obj = DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data_path, test_data_path)