from .GlobalVariables import *
import pandas as pd
import numpy as np


def is_digit(string):
    return string in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def retrieve_numbers_ACS(column):
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
            if is_digit(value[i]) and can_start_again:
                number += value[i]
            else:
                if number != '' and (i+1) < len(value) and (''+value[i]+value[i+1]) == ' -':
                    if not (number in array):
                        array.append(number)
                    can_start_again = False
                number = ''
    return array


def retrieve_array_of_numbers(column):
    array = []
    for value in column:
        if pd.isna(value):
            continue
        number = ''
        seq = False
        for i in range(0, len(value)):
            if is_digit(value[i]):
                number += value[i]
                seq = True
            else:
                seq = False
            if (not seq) and (number != ''):
                if not (number in array):
                    array.append(number)
                number = ''
    return array


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


def create_dataframe(data, column_name, prefix, ACS):
    if ACS:
        cod = retrieve_numbers_ACS(data[column_name])
    else:
        cod = retrieve_array_of_numbers(data[column_name])
    prefix_cod = cod.copy()

    for i in range(0, len(prefix_cod)):
        prefix_cod[i] = prefix + prefix_cod[i]

    default_matrix = np.zeros(shape=(data.shape[0], len(prefix_cod)), dtype=np.int32)

    matrix = pd.DataFrame(data=default_matrix,
                                       columns=prefix_cod,
                                       index=np.arange(0, default_matrix.shape[0])
                                       )

    return check_and_change_dataframe(data[column_name], matrix, prefix_cod, cod)

def checkForMistake(string):
    for i in range(0,len(string)):
        if (not is_digit(string[i])) and (not (string[i] == '.')):
            return True
    return False


DATASET_NAME = 'ipodata.xlsx'
SHEET_NAME = 'Folha1'

data = pd.read_excel(DATASET_NAME, sheet_name=SHEET_NAME, dtype=str, header=1)

data.rename(columns={data.columns[136]: 'Comorbilidades pré-operatórias'}, inplace=True)

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
        if column in NUMERICAL_CONTINUOUS:
            if ',' in value:
                data.at[index, column] = value.replace(',', '.')
        index += 1


data.rename(columns={'risco médio': 'risco médio - complicações sérias (%)',
                     'risco médio.1': 'risco médio - qualquer complicação (%)',
                     'risco médio.2': 'risco médio - pneumonia (%)',
                     'risco médio.3': 'risco médio - complicações cardíacas (%)',
                     'risco médio.4': 'risco médio - infeção cirúrgica (%)',
                     'risco médio.5': 'risco médio - ITU (%)',
                     'risco médio.6': 'risco médio - tromboembolismo venoso (%)',
                     'risco médio.7': 'risco médio - falência renal (%)',
                     'risco médio.8': 'risco médio - ileus (%)',
                     'risco médio.9': 'risco médio - fuga anastomótica (%)',
                     'risco médio.10': 'risco médio - readmissão (%)',
                     'risco médio.11': 'risco médio - reoperação (%)',
                     'risco médio.12': 'risco médio - morte (%)',
                     'risco médio.13': 'risco médio - Discharge to Nursing or Rehab Facility (%)'
                     }, inplace=True)

#data.drop(columns=['data pedido anestesia'])

for column in data.columns:
    if column in NUMERICAL_CONTINUOUS:
        index = 0
        for value in data[column]:
            if pd.isna(value):
                index += 1
                continue
            new_value = ''
            second_comma = False
            for i in range(0, len(value)):
                if is_digit(value[i]):
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
    if column in NUMERICAL_DISCRETE or\
    column in NUMERICAL_CONTINUOUS or\
    column in CATEGORICAL or\
    column in BINARY:
        index = 0
        for value in data[column]:
            if pd.isna(value) or (not checkForMistake(value)):
                index += 1
            else:
                data.at[index, column] = 'NaN'
                index += 1

intervencoes_matrix = create_dataframe(data, 'Intervenções_ICD10', 'ICD_', False)
acs_proc = create_dataframe(data, 'ACS_procedimento', 'ACS_', True)
ce_matrix = create_dataframe(data, 'classificação ACS complicações específicas', 'ACS_CE_', False)

data = pd.concat([data, intervencoes_matrix, ce_matrix, acs_proc], axis=1, sort=False)

data.to_csv('data.csv', index=False)
print('done')
