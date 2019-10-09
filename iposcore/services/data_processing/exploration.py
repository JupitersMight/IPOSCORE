import pandas as pd
from services.data_processing.utils import Utils
from data.global_variables import GlobalVariables
from scipy.stats import sem, t
from scipy import mean
import json


class DataExploration:

    class column_value_counter:
        def __init__(self, name, counter):
            self.name = name
            self.counter = counter

    @staticmethod
    def checkprefix(value, prefixs):
        for prefix in prefixs:
            if prefix in value:
                return True
        return False

    @staticmethod
    def explore(data):
        # Setup for json data
        json_data = {
            'Binary': {},
            'Categorical': {},
            'Numerical_Discrete': {},
            'Numerical_Continuous': {}
        }
        # Populate with attribute names
        for value in GlobalVariables.DatasetColumns.binary:
            json_data['Binary'][value] = {}
        for value in GlobalVariables.DatasetColumns.categorical:
            json_data['Categorical'][value] = {}
        for value in GlobalVariables.DatasetColumns.numerical_discrete:
            json_data['Numerical_Discrete'][value] = {}
        for value in GlobalVariables.DatasetColumns.numerical_continuous:
            json_data['Numerical_Continuous'][value] = {}

        # Fill attribute with number of missings
        missings = DataExploration.number_of_missing_values(data)
        for value in missings:
            if value[0] in GlobalVariables.DatasetColumns.binary \
                    or DataExploration.checkprefix(value[0], GlobalVariables.DatasetColumns.prefix_for_generated_columns)\
                    or value[0] == GlobalVariables.DatasetColumns.class_label[0]:
                json_data['Binary'][value[0]]['missings'] = value[1]
            if value[0] in GlobalVariables.DatasetColumns.categorical \
                    or GlobalVariables.DatasetColumns.class_label[1]:
                json_data['Categorical'][value[0]]['missings'] = value[1]
            if value[0] in GlobalVariables.DatasetColumns.numerical_discrete:
                json_data['Numerical_Discrete'][value[0]]['missings'] = value[1]
            if value[0] in GlobalVariables.DatasetColumns.numerical_continuous:
                json_data['Numerical_Continuous'][value[0]]['missings'] = value[1]

        for column in data.columns:
            if column in GlobalVariables.DatasetColumns.numerical_continuous \
                    or column in GlobalVariables.DatasetColumns.text\
                    or column in GlobalVariables.DatasetColumns.ignored_columns\
                    or column in GlobalVariables.DatasetColumns.dates:
                continue
            values = DataExploration.distribution(data[column])
            if column in GlobalVariables.DatasetColumns.binary or DataExploration.checkprefix(column, GlobalVariables.DatasetColumns.prefix_for_generated_columns):
                for value in values:
                    json_data['Binary'][column]['distribution'][value.name] = value.counter
            elif column in GlobalVariables.DatasetColumns.categorical:
                for value in values:
                    json_data['Categorical'][column]['distribution'][value.name] = value.counter
            elif column in GlobalVariables.DatasetColumns.numerical_discrete:
                for value in values:
                    json_data['Numerical_Discrete'][column]['distribution'][value.name] = value.counter

        for column in data.columns:
            if column in GlobalVariables.DatasetColumns.numerical_continuous:
                filtered_data = data[column].dropna()
                confidence = 0.95
                n = len(filtered_data)
                m = mean(filtered_data)
                std_err = sem(filtered_data)
                h = std_err * t.ppf((1 + confidence) / 2, n - 1)
                json_data['Numerical_Continuous'][column]['confidence_interval'] = {
                    'start': (m - h),
                    'finish': (m + h)
                }
                json_data['Numerical_Continuous'][column]['mean'] = m


    @staticmethod
    def number_of_missing_values(dataset):
        missing_values = []
        for column_name in dataset.columns:
            counter = 0
            for value in dataset[column_name]:
                if not pd.isna(value):
                    continue
                counter += 1
            missing_values.append([column_name, counter])
        return missing_values

    @staticmethod
    def distribution(column):
        different_values = []
        for value in column:
            if pd.isna(value):
                continue
            is_in_array = False
            for i in range(len(different_values)):
                if value == different_values[i].name:
                    is_in_array = True
                    different_values[i].counter += 1
                    break
            if not is_in_array:
                different_values.append(DataExploration.column_value_counter(value, 1))
        return different_values

























