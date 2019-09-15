import pandas as pd
from services.data_manager.utils import Utils
from data.global_variables import GlobalVariables
import os.path as path
from pathlib import Path


class DataClean:

    @staticmethod
    def clean_data():
        DATASET_NAME = 'ipodata.xlsx'
        SHEET_NAME = 'Folha1'

        directory = Path(__file__).resolve().parents[2]

        data = pd.read_excel(path.join(directory, 'data', DATASET_NAME), sheet_name=SHEET_NAME, dtype=str, header=1)

        data.rename(columns={data.columns[136]: 'Comorbilidades pré-operatórias'}, inplace=True)

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

        Utils.change_to_default_na(data)

        data = Utils.normalize_values(data)

        intervencoes_matrix = Utils.create_dataframe(data, 'Intervenções_ICD10', 'ICD_', False)
        acs_proc = Utils.create_dataframe(data, 'ACS_procedimento', 'ACS_', True)
        ce_matrix = Utils.create_dataframe(data, 'classificação ACS complicações específicas', 'ACS_CE_', False)

        data = pd.concat([data, intervencoes_matrix, ce_matrix, acs_proc], axis=1, sort=False)

        data.to_csv(path.abspath(path.join(directory, 'data', 'post_clean.csv')), index=False)
