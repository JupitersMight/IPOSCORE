import numpy as np
import pandas as pd


class Utils:

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

