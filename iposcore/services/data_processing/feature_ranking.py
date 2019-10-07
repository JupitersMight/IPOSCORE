import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression, chi2
from sklearn.feature_extraction.text import CountVectorizer
from data.global_variables import GlobalVariables
import json


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

def retrieveValues(array, index):
    colunas = []
    valores = []
    for value in array:
        if value[1] == 0:
            continue
        colunas.append(value[0])
        valores.append(value[index])
    aux = sort(colunas, valores)
    aux[0] = aux[0][:10]
    aux[1] = aux[1][:10]
    return aux


class FeatureRanking:

    @staticmethod
    def feature_ranking(data, columns, class_label):
        final_data = {}
        for label in class_label:
            binary_m = []
            categorical_m = []
            numerical_discrete_m = []
            numerical_continuous_m = []
            text = []
            class_data = data[label]
            data.drop(columns=[label])

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
                             labels[label]
                         )[0],
                         mutual_info_regression(
                             labels[column].to_frame(name=column),
                             labels[label]
                         )[0],
                         chi2(
                             labels[column].to_frame(name=column),
                             labels[label]
                         )
                         ]
                    )
                elif column in GlobalVariables.DatasetColumns.categorical:
                    categorical_m.append(
                        [column,
                         mutual_info_classif(
                             labels[column].to_frame(name=column),
                             labels[label]
                         )[0],
                         mutual_info_regression(
                             labels[column].to_frame(name=column),
                             labels[label]
                         )[0],
                         chi2(
                             labels[column].to_frame(name=column),
                             labels[label]
                         )
                         ]
                    )
                elif column in GlobalVariables.DatasetColumns.numerical_discrete:
                    numerical_discrete_m.append(
                        [column,
                         mutual_info_classif(
                             labels[column].to_frame(name=column),
                             labels[label]
                         )[0],
                         mutual_info_regression(
                             labels[column].to_frame(name=column),
                             labels[label]
                         )[0],
                         chi2(
                             labels[column].to_frame(name=column),
                             labels[label]
                         )
                         ]
                    )
                elif column in GlobalVariables.DatasetColumns.numerical_continuous:
                    numerical_continuous_m.append(
                        [column,
                         mutual_info_classif(
                             labels[column].to_frame(name=column),
                             labels[label]
                         )[0],
                         mutual_info_regression(
                             labels[column].to_frame(name=column),
                             labels[label]
                         )[0],
                         chi2(
                             labels[column].to_frame(name=column),
                             labels[label]
                         )
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
                                labels[label],
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
            column_types = ['Binary', 'Categorical', 'Numerical_Discrete', 'Numerical_Contiguous']
            classifiers = ['mutual_info_classif', 'mutual_info_regression']#, 'chi2']
            index = 0
            temp = {}
            for array in arrays:
                classif_index = 1
                temp['' + column_types[index]] = {}
                for classif in classifiers:
                    aux = retrieveValues(array, classif_index)
                    temp[''+column_types[index]][''+classifiers[classif_index-1]] = []
                    i = 0
                    for value in aux[0]:
                        x = {
                            'column_name': aux[0][i],
                            'column_value': aux[1][i]
                        }
                        temp[''+column_types[index]][''+classifiers[classif_index-1]].append(x)
                        i += 1
                    classif_index += 1
                index += 1
            final_data['' + label] = temp

        return json.dumps(final_data)
