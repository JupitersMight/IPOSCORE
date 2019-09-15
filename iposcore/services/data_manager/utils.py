import pandas as pd
import numpy as np
from data.global_variables import GlobalVariables

class Utils:

    @staticmethod
    def is_digit(string):
        return string in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    @staticmethod
    def retrieve_numbers_acs(column):
        array = []
        for value in column:
            if pd.isna(value):
                continue
            number = ''
            can_start_again = True
            start_seq = False
            for i in range(0, len(value)):
                if value[i] == '+':
                    can_start_again = True
                if Utils.is_digit(value[i]) and can_start_again:
                    number += value[i]
                else:
                    if number != '' and (i + 1) < len(value) and ('' + value[i] + value[i + 1]) == ' -':
                        if not (number in array):
                            array.append(number)
                        can_start_again = False
                    number = ''
        return array

    @staticmethod
    def retrieve_array_of_numbers(column):
        array = []
        for value in column:
            if pd.isna(value):
                continue
            number = ''
            seq = False
            for i in range(0, len(value)):
                if Utils.is_digit(value[i]):
                    number += value[i]
                    seq = True
                else:
                    seq = False
                if (not seq) and (number != ''):
                    if not (number in array):
                        array.append(number)
                    number = ''
        return array

    @staticmethod
    def check_and_change_dataframe(column, dataframe, dataframe_columns, values):
        index = 0
        for value in column:
            if pd.isna(value):
                index += 1
                continue
            for i in range(0, len(dataframe_columns)):
                if values[i] in value:
                    dataframe.at[index, dataframe_columns[i]] = 1
            index += 1
        return dataframe

    @staticmethod
    def create_dataframe(data, column_name, prefix, ACS):
        if ACS:
            cod = Utils.retrieve_numbers_acs(data[column_name])
        else:
            cod = Utils.retrieve_array_of_numbers(data[column_name])
        prefix_cod = cod.copy()

        for i in range(0, len(prefix_cod)):
            prefix_cod[i] = prefix + prefix_cod[i]

        default_matrix = np.zeros(shape=(data.shape[0], len(prefix_cod)), dtype=np.int32)

        matrix = pd.DataFrame(data=default_matrix,
                              columns=prefix_cod,
                              index=np.arange(0, default_matrix.shape[0])
                              )

        return Utils.check_and_change_dataframe(data[column_name], matrix, prefix_cod, cod)

    @staticmethod
    def check_if_number_valid(string):
        for i in range(0, len(string)):
            if (not Utils.is_digit(string[i])) and (not (string[i] == '.')):
                return True
        return False

    @staticmethod
    def change_to_default_na(data):
        for column in data.columns:
            index = 0
            for value in data[column]:
                if pd.isna(value):
                    index += 1
                    continue
                if 'sem dados' in value or 'indefinido' in value or 'n/a' in value:
                    data.at[index, column] = 'NaN'
                if '%' in value:
                    data.at[index, column] = value.replace('%', '')
                if column in GlobalVariables.DatasetColumns.numerical_continuous:
                    if ',' in value:
                        data.at[index, column] = value.replace(',', '.')
                index += 1

        return data

    @staticmethod
    def normalize_values(data):
        for column in data.columns:
            if column in GlobalVariables.DatasetColumns.numerical_continuous:
                index = 0
                for value in data[column]:
                    if pd.isna(value):
                        index += 1
                        continue
                    new_value = ''
                    second_comma = False
                    for i in range(0, len(value)):
                        if Utils.is_digit(value[i]):
                            new_value += value[i]
                        elif value[i] == '.' or value[i] == ',':
                            if second_comma:
                                break
                            else:
                                new_value += '.'
                                second_comma = True
                    data.at[index, column] = new_value
                    index += 1

        for column in data.columns:
            if column in GlobalVariables.DatasetColumns.numerical_discrete or\
                column in GlobalVariables.DatasetColumns.numerical_continuous or\
                column in GlobalVariables.DatasetColumns.categorical or\
                    column in GlobalVariables.DatasetColumns.binary:
                index = 0
                for value in data[column]:
                    if pd.isna(value) or (not Utils.check_if_number_valid(value)):
                        index += 1
                    else:
                        data.at[index, column] = 'NaN'
                        index += 1

        return data
