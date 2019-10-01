import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.feature_extraction.text import CountVectorizer
from data.global_variables import GlobalVariables


def sort(colunas,valores):
    novas_colunas = []
    novos_valores = []

    while len(valores) != 0:
        index = 0
        curr_maximo = 0
        curr_index = 0
        for valor in valores:
            if valor > curr_maximo:
                curr_maximo = valor
                curr_index = index
            index += 1
        novas_colunas.append(colunas[curr_index])
        novos_valores.append(curr_maximo)
        del colunas[curr_index]
        del valores[curr_index]
    return [novas_colunas, novos_valores]


class FeatureRanking:

    @staticmethod
    def feature_ranking(data, columns, class_label):
        binary_m = []
        categorical_m = []
        numerical_discrete_m = []
        numerical_continuous_m = []
        text = []

        class_data = data[class_label]
        data.drop(columns=[class_label])

        joined_array = []
        for array in columns:
            joined_array = joined_array + array

        for column in joined_array:
            true_label = class_data.__deepcopy__()
            pred_label = data[column]

            labels = pd.concat([true_label, pred_label], axis=1, sort=False)
            labels = labels.dropna()
            labels = labels.reset_index(drop=True)

            if column in GlobalVariables.DatasetColumns.binary:
                binary_m.append(
                    [column,
                     mutual_info_classif(
                         labels[column].to_frame(name=column),
                         labels[GlobalVariables.DatasetColumns.class_label]
                     )[0]
                     ]
                )
            elif column in GlobalVariables.DatasetColumns.categorical:
                categorical_m.append(
                    [column,
                     mutual_info_classif(
                         labels[column].to_frame(name=column),
                         labels[GlobalVariables.DatasetColumns.class_label]
                     )[0]
                     ]
                )
            elif column in GlobalVariables.DatasetColumns.numerical_discrete:
                numerical_discrete_m.append(
                    [column,
                     mutual_info_classif(
                         labels[column].to_frame(name=column),
                         labels[GlobalVariables.DatasetColumns.class_label]
                     )[0]
                     ]
                )
            elif column in GlobalVariables.DatasetColumns.numerical_continuous:
                numerical_continuous_m.append(
                    [column,
                     mutual_info_classif(
                         labels[column].to_frame(name=column),
                         labels[GlobalVariables.DatasetColumns.class_label]
                     )[0]
                     ]
                )
            elif column in GlobalVariables.DatasetColumns.text:
                cv = CountVectorizer(max_df=0.95, min_df=2, max_features=10000)

                X_vec = cv.fit_transform(labels[column])

                dictionary = dict(
                    zip(
                        cv.get_feature_names(),
                        mutual_info_classif(
                            X_vec,
                            labels[GlobalVariables.DatasetColumns.class_label],
                            discrete_features=True
                        )
                    )
                )

                colunas = []
                valores = []
                for col, val in dictionary.items():
                    if val == 0:
                        continue
                    colunas.append(col)
                    valores.append(val)

                aux = sort(colunas, valores)
                aux[0] = aux[0][:10]
                aux[1] = aux[1][:10]
                text.append(aux)

        arrays = [binary_m, categorical_m, numerical_discrete_m, numerical_continuous_m]
        index = 0
        for array in arrays:
            colunas = []
            valores = []
            for value in array:
                if value[1] == 0:
                    continue
                colunas.append(value[0])
                valores.append(value[1])
            aux = sort(colunas, valores)
            aux[0] = aux[0][:10]
            aux[1] = aux[1][:10]
            arrays[index] = aux
            index = index + 1
        arrays.append(text)
        return arrays
