import numpy as np
import pandas as pd


class Utils:

    class data_column:
        def __init__(self, name, age):
            self.name = name
            self.counter = age

    @staticmethod
    def preprocess_substitute_na_with_average(dataset):
        list_of_columns = dataset.columns
        array_of_mean_values = []
        for column_name in list_of_columns:
            if column_name == "class":
                continue
            list_of_items = dataset[column_name]

            array_of_mean_values.append(Utils.calculate_mean_with_na(list_of_items))

        i = 0

        for column_name in list_of_columns:
            if column_name == "class":
                continue
            dataset[column_name].fillna(str(array_of_mean_values[i]))
            i += 1

    @staticmethod
    def calculate_mean_with_na(list):
        sum_value = 0
        counter = 0
        for value in list:
            if value != "na":
                if isinstance(value, str):
                    value = float(value)
                sum_value = sum_value + value
                counter += 1
        return sum_value / counter

    @staticmethod
    def calculate_mean(dataset):
        mean_values = []
        for column_name in dataset.columns:
            if column_name == "class":
                continue
            sum_values = 0
            i = 0
            for value in dataset[column_name]:
                if value == 'n/a':
                    continue
                sum_values += float(value)
                i += 1
            mean_values.append(str(sum_values / i))
        return mean_values

    @staticmethod
    def distribution(column):
        different_values = []
        for value in column:
            if value == 'n/a':
                continue
            isInArray = False
            for i in range(len(different_values)):
                if value == different_values[i].name:
                    isInArray = True
                    different_values[i].counter += 1
                    break
            if not isInArray:
                different_values.append(Utils.data_column(value, 1))
        return different_values

    @staticmethod
    def number_of_missing_values(dataset):
        missing_values = []
        for column_name in dataset.columns:
            counter = 0
            for value in dataset[column_name]:
                if value != 'n/a':
                    continue
                counter += 1
            missing_values.append(counter)
        return missing_values

    @staticmethod
    def calculate_meadian(dataset):
        median_values = []
        for column_name in dataset.columns:
            if column_name == "class":
                continue
            values = []
            for value in dataset[column_name]:
                if value == 'n/a':
                    continue
                values.append(float(value))
            median_values.append(np.median(values))
        return median_values

    @staticmethod
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

    @staticmethod
    def normalize_values(column):
        min_value = 0
        max_value = 0
        first_value = 1
        for value in column:
            if value == 'na':
                continue
            if first_value == 1:
                min_value = float(value)
                max_value = float(value)
                first_value = 0
            if min_value > float(value):
                min_value = float(value)
            if max_value < float(value):
                max_value = float(value)
        result = []
        for value in column:
            if value == 'na':
                continue
            if max_value - min_value > 0:
                result.append((float(value) - min_value) / (max_value - min_value))

        return result

