import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.utils import save_object
from src.exception import CustomException
from src.logger import logging
import os

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_features = ["writing score","reading score"]
            categorical_features = ["gender","race/ethnicity","parental level of education", "lunch", "test preparation course"]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy='most_frequent')),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            logging.info("Numerical Column strandard scaling completed")
            logging.info("categorical Column encoding completed")

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_features),
                    ("cat_pipeline", cat_pipeline, categorical_features)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining Pre Processor Object")
            preprocessor_obj = self.get_data_transformer_object()

            target_column = "math score"
            input_feature_train = train_df.drop(columns=[target_column], axis=1)
            target_feature_train = train_df[target_column] 

            input_feature_test = test_df.drop(columns=[target_column], axis=1)
            target_feature_test = test_df[target_column] 

            input_feature_train_array = preprocessor_obj.fit_transform(input_feature_train)
            input_feature_test_array = preprocessor_obj.transform(input_feature_test)

            train_arr = np.c_[input_feature_train_array, np.array(target_feature_train)]
            test_arr = np.c_[input_feature_test_array, np.array(target_feature_test)]
            
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
