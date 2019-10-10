import pandas as pd
from data.global_variables import GlobalVariables
from scipy.stats import sem, t
from scipy import mean
import numpy as np
import json


class column_value_counter:
    def __init__(self, name, counter):
        self.name = name
        self.counter = counter


def checkprefix(value, prefixs):
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
            different_values.append(column_value_counter(value, 1))
    return different_values


def calculate_meadian(column):
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
            if checkprefix(value, GlobalVariables.DatasetColumns.prefix_for_generated_columns):
                json_data['Binary'][value] = {}

        # Fill attribute with number of missings
        missings = number_of_missing_values(data)
        for value in missings:
            if value[0] in GlobalVariables.DatasetColumns.binary \
                    or checkprefix(value[0], GlobalVariables.DatasetColumns.prefix_for_generated_columns)\
                    or value[0] == GlobalVariables.DatasetColumns.class_label[0]:
                json_data['Binary'][value[0]]['missings'] = value[1]
            elif value[0] in GlobalVariables.DatasetColumns.categorical \
                    or value[0] == GlobalVariables.DatasetColumns.class_label[1]:
                json_data['Categorical'][value[0]]['missings'] = value[1]
            elif value[0] in GlobalVariables.DatasetColumns.numerical_discrete:
                json_data['Numerical_Discrete'][value[0]]['missings'] = value[1]
            elif value[0] in GlobalVariables.DatasetColumns.numerical_continuous:
                json_data['Numerical_Continuous'][value[0]]['missings'] = value[1]

        for column in data.columns:
            if column in GlobalVariables.DatasetColumns.numerical_continuous \
                    or column in GlobalVariables.DatasetColumns.text\
                    or column in GlobalVariables.DatasetColumns.ignored_columns\
                    or column in GlobalVariables.DatasetColumns.dates\
                    or column in GlobalVariables.DatasetColumns.numerical_discrete:
                continue
            values = distribution(data[column])
            if column in GlobalVariables.DatasetColumns.binary or checkprefix(column, GlobalVariables.DatasetColumns.prefix_for_generated_columns):
                json_data['Binary'][column]['distribution'] = {}
                for value in values:
                    json_data['Binary'][column]['distribution'][value.name] = value.counter
            elif column in GlobalVariables.DatasetColumns.categorical:
                json_data['Categorical'][column]['distribution'] = {}
                for value in values:
                    json_data['Categorical'][column]['distribution'][value.name] = value.counter

        for column in data.columns:
            data_type = ''
            if column in GlobalVariables.DatasetColumns.numerical_continuous:
                data_type = 'Numerical_Continuous'
            elif column in GlobalVariables.DatasetColumns.numerical_discrete:
                data_type = 'Numerical_Discrete'
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
                json_data[data_type][column]['median'] = calculate_meadian(filtered_data)
                json_data[data_type][column]['standard_deviation'] = np.std(filtered_data)

        for column in data.columns:
            data_type = ''
            #if column in GlobalVariables.DatasetColumns.binary or checkprefix(column, GlobalVariables.DatasetColumns.prefix_for_generated_columns):
                #data_type = 'Binary'
            if column in GlobalVariables.DatasetColumns.numerical_continuous:
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
                    json_data[data_type][column]['dataset'].append({
                        '' + column: row.iloc[0][column],
                        GlobalVariables.DatasetColumns.class_label[0]: row.iloc[0][
                            GlobalVariables.DatasetColumns.class_label[0]],
                        GlobalVariables.DatasetColumns.class_label[1]: row.iloc[0][
                            GlobalVariables.DatasetColumns.class_label[1]]
                    })

        return json.dumps(json_data)
