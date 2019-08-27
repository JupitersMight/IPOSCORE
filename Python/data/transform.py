import numpy as np
import pandas as pd
import math
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing
from scipy.stats import sem, t

def is_digit(string):
    return string in ['1','2','3','4','5','6','7','8','9']


def retrieve_array_of_numbers(column):
    array = []
    for value in column:
        number = ''
        seq = False
        for i in range(0, len(value)):
            if is_digit(value[i]):
                number.join(value[i])
                seq = True
            else:
                seq = False
            if not seq and number != '':
                if not (number in array):
                    array.append(number)
                number = ''
    return array

def check_and_change_dataframe(column, dataframe, dataframe_columns, values):
    index = 0
    for value in column:
        for i in range(0, len(dataframe_columns)):
            if values[i] in value:
                dataframe.loc[index, dataframe_columns[i]] = 1
        index += 1
    return dataframe


DATASET_NAME = 'cleanedData.csv'

data = pd.read_excel(DATASET_NAME, delimiter=',', na_values=['n/a']).drop(columns=['especialidade', 'data pedido anestesia'])

cod = retrieve_array_of_numbers(data['Intervenções_ICD10'])
intervencoes_cod = cod

default_column = []

for i in range(0, len(data['Intervenções_ICD10'])):
    default_column.append(0)

default_matrix = []

for i in range(0, len(intervencoes_cod)):
    default_matrix.append(default_column)

for i in range(0, len(intervencoes_cod)):
    intervencoes_cod[i] = 'ICD' + intervencoes_cod[i]

intervencoes_matrix = pd.DataFrame(np.array(default_matrix), columns=intervencoes_cod)

intervencoes_matrix = check_and_change_dataframe(data['Intervenções_ICD10'], intervencoes_matrix, intervencoes_cod, cod)

data = data.join(intervencoes_matrix)

x=0



