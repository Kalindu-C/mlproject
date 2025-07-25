import sys
from dataclasses import dataclass

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer # used to create a pipeline for preprocessing
from sklearn.impute import SimpleImputer # used to handle missing values
from sklearn.pipeline import Pipeline # used to create a pipeline for preprocessing
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):

        '''
        This function is responsible for creating the data transformation pipeline.

        '''
        try:
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            logging.info("Numerical columns and categorical columns defined")

            # Numerical pipeline
            numerical_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ])

            # Categorical pipeline
            categorical_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ])

            logging.info("Numerical and categorical pipelines created")

            preprocessor = ColumnTransformer(
                [
                    ('num', numerical_pipeline, numerical_columns),
                    ('cat', categorical_pipeline, categorical_columns)
                ]
            )

            logging.info("Column transformer created")

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
        
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info("Initiating data transformation")
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            logging.info("Data loaded successfully")

            preprocessing_obj = self.get_data_transformer_object()

            logging.info("Data transformation pipeline created")

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_data.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_data[target_column_name]

            input_feature_test_df=test_data.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_data[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )


        except Exception as e:
            raise CustomException(e, sys)