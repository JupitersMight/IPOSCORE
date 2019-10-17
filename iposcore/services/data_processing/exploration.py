import pandas as pd
from data.global_variables import GlobalVariables
from scipy.stats import sem, t
from scipy import mean
import numpy as np
import json


def check_prefix(value, prefixs):
    for prefix in prefixs:
        if prefix in value:
            return True
    return False


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


def calculate_median(column):
    values = []
    for value in column:
        if pd.isna(value):
            continue
        values.append(value)
    return np.median(values)


def number_of_outliers(vector):
    vector = pd.Series(vector)
    Q1 = vector.quantile(0.25)
    Q3 = vector.quantile(0.75)
    IQR = Q3 - Q1
    low_interval = Q1 - 1.5 * IQR
    high_interval = Q3 + 1.5 * IQR
    counter = 0
    for value in vector:
        if value < low_interval:
            counter += 1
        if value > high_interval:
            counter += 1
    return counter


class DataExploration:

    @staticmethod
    def explore(data):
        data = data.drop(columns=GlobalVariables.DatasetColumns.dates)
        data = data.drop(columns=GlobalVariables.DatasetColumns.ignored_columns)
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
        json_data['Binary'][GlobalVariables.DatasetColumns.class_label[0]] = {}
        json_data['Categorical'][GlobalVariables.DatasetColumns.class_label[1]] = {}
        for value in data.columns:
            if check_prefix(value, GlobalVariables.DatasetColumns.prefix_for_generated_columns):
                json_data['Binary'][value] = {}

        # Fill json attributes with number of missings
        missings = number_of_missing_values(data)
        for value in missings:
            if value[0] in GlobalVariables.DatasetColumns.binary \
                    or check_prefix(value[0], GlobalVariables.DatasetColumns.prefix_for_generated_columns)\
                    or value[0] == GlobalVariables.DatasetColumns.class_label[0]:
                json_data['Binary'][value[0]]['missings'] = value[1]
            elif value[0] in GlobalVariables.DatasetColumns.categorical \
                    or value[0] == GlobalVariables.DatasetColumns.class_label[1]:
                json_data['Categorical'][value[0]]['missings'] = value[1]
            elif value[0] in GlobalVariables.DatasetColumns.numerical_discrete:
                json_data['Numerical_Discrete'][value[0]]['missings'] = value[1]
            elif value[0] in GlobalVariables.DatasetColumns.numerical_continuous:
                json_data['Numerical_Continuous'][value[0]]['missings'] = value[1]

        # Fill json attributes with confidence intervals, mean, standard deviation and median
        for column in data.columns:
            data_type = ''
            if column in GlobalVariables.DatasetColumns.binary or check_prefix(column, GlobalVariables.DatasetColumns.prefix_for_generated_columns):
                data_type = 'Binary'
            if column in GlobalVariables.DatasetColumns.numerical_continuous:
                data_type = 'Numerical_Continuous'
            elif column in GlobalVariables.DatasetColumns.numerical_discrete:
                data_type = 'Numerical_Discrete'
            elif column in GlobalVariables.DatasetColumns.categorical:
                data_type = 'Categorical'
            if data_type != '':
                filtered_data = data[column].dropna().to_numpy()
                index = 0
                for value in filtered_data:
                    filtered_data[index] = float(value)
                    index += 1
                confidence = 0.95
                n = len(filtered_data)
                m = mean(filtered_data)
                std_err = sem(filtered_data)
                h = std_err * t.ppf((1 + confidence) / 2, n - 1)

                json_data[data_type][column]['confidence_interval'] = {
                    'start': (m - h),
                    'finish': (m + h)
                }
                json_data[data_type][column]['mean'] = m
                json_data[data_type][column]['median'] = calculate_median(filtered_data)
                json_data[data_type][column]['standard_deviation'] = np.std(filtered_data)

        # Fill json attributes with dataset of attribute value and corresponding class labels
        for column in data.columns:
            data_type = ''
            if column in GlobalVariables.DatasetColumns.binary or check_prefix(column, GlobalVariables.DatasetColumns.prefix_for_generated_columns):
                data_type = 'Binary'
            elif column in GlobalVariables.DatasetColumns.numerical_continuous:
                data_type = 'Numerical_Continuous'
            elif column in GlobalVariables.DatasetColumns.numerical_discrete:
                data_type = 'Numerical_Discrete'
            elif column in GlobalVariables.DatasetColumns.categorical:
                data_type = 'Categorical'
            if data_type != '':
                aux = data[[column, GlobalVariables.DatasetColumns.class_label[0],
                            GlobalVariables.DatasetColumns.class_label[1]]].dropna().reset_index()
                json_data[data_type][column]['dataset'] = []
                for index in range(0, aux.shape[0]):
                    row = aux.iloc[[index]]
                    column_value = row.iloc[0][column]
                    class_label_1_name = GlobalVariables.DatasetColumns.class_label[0]
                    class_label_2_name = GlobalVariables.DatasetColumns.class_label[1]
                    class_label_1_value = row.iloc[0][GlobalVariables.DatasetColumns.class_label[0]]
                    class_label_2_value = row.iloc[0][GlobalVariables.DatasetColumns.class_label[1]]

                    json_data[data_type][column]['dataset'].append({
                        column: column_value,
                        class_label_2_name: class_label_2_value,
                        class_label_1_name: class_label_1_value
                    })

        return json.dumps(json_data)
