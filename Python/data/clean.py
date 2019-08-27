import pandas as pd


def is_digit(string):
    return string in ['1','2','3','4','5','6','7','8','9']


def check_and_replace_mistakes_in_numerical_columns(data):
    for column in data.columns:
        if column in NUMERICAL_WITH_DECIMALS_COLUMNS:
            index = 0
            for value in data[column]:
                if pd.isna(value):
                    index += 1
                    continue
                new_value = ''
                second_comma = False
                for i in range(0, len(value)):
                    if is_digit(value[i]):
                        new_value.join(value[i])
                    elif value[i] == '.' or value[i] == ',':
                        if second_comma:
                            break
                        else:
                            new_value.join('.')
                            second_comma = True
                data.loc[index, column] = new_value
                index += 1
    return data


DATASET_NAME = 'BaseDados_08.03.2019_IPOscore.xlsx'
SHEET_NAME = 'Folha1'
NUMERICAL_WITH_DECIMALS_COLUMNS = ['dias na UCI',
                                   'total pontos NAS',
                                   'pontos NAS por dia',
                                   '% morbilidade P-Possum',
                                   '% mortalidade P-Possum',
                                   'ACS peso',
                                   'complicações sérias (%)',
                                   'qualquer complicação (%)',
                                   'pneumonia (%)',
                                   'complicações cardíacas (%)',
                                   'infeção cirúrgica (%)',
                                   'ITU (%)',
                                   'tromboembolismo venoso (%)',
                                   'falência renal (%)',
                                   'ileus (%)',
                                   'fuga anastomótica (%)',
                                   'readmissão (%)',
                                   'reoperação (%)',
                                   'morte (%)',
                                   'Discharge to Nursing or Rehab Facility (%)',
                                   'risco médio - complicações sérias (%)',
                                   'risco médio - qualquer complicação (%)',
                                   'risco médio - pneumonia (%)',
                                   'risco médio - complicações cardíacas (%)',
                                   'risco médio - infeção cirúrgica (%)',
                                   'risco médio - ITU (%)',
                                   'risco médio - tromboembolismo venoso (%)',
                                   'risco médio - falência renal (%)',
                                   'risco médio - ileus (%)',
                                   'risco médio - fuga anastomótica (%)',
                                   'risco médio - readmissão (%)',
                                   'risco médio - reoperação (%)',
                                   'risco médio - morte (%)',
                                   'risco médio - Discharge to Nursing or Rehab Facility (%)',
                                   'ACS - previsão dias internamento'
                                   ]

data = pd.read_excel(DATASET_NAME, sheet_name=SHEET_NAME, dtype=str)

data.replace({'sem dados': 'n/a'}, regex=True)
data.replace({'indefinido': 'n/a'}, regex=True)
data.replace({'%': ''}, regex=True)


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

data = check_and_replace_mistakes_in_numerical_columns(data)

data.to_csv('cleanedData.csv', index=False)
