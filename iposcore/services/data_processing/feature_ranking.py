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
    def numerical_continuous(data, columns, class_label):
        numerical_continuous_m = []

        class_data = data[class_label]
        data.drop(columns=[class_label])

        for column in columns:
            true_label = class_data.__deepcopy__()
            pred_label = data[column]

            labels = pd.concat([true_label, pred_label], axis=1, sort=False)
            labels = labels.dropna()
            labels = labels.reset_index(drop=True)
            numerical_continuous_m.append(
                [column,
                 mutual_info_regression(
                     labels[column].to_frame(name=column),
                     labels[GlobalVariables.DatasetColumns.class_label]
                 )[0]]
            )

        colunas = []
        valores = []
        for value in numerical_continuous_m:
            if (int(value[1] * 100)) == 0:
                continue
            colunas.append(value[0])
            valores.append(int(value[1] * 100))
        aux = sort(colunas, valores)
        aux[0] = aux[0][:10]
        aux[1] = aux[1][:10]
        return aux

    @staticmethod
    def numerical_discrete(data, columns, class_label):
        numerical_discrete_m = []

        class_data = data[class_label]
        data.drop(columns=[class_label])
        for column in columns:
            true_label = class_data.__deepcopy__()
            pred_label = data[column]

            labels = pd.concat([true_label, pred_label], axis=1, sort=False)
            labels = labels.dropna()
            labels = labels.reset_index(drop=True)

            numerical_discrete_m.append(
                [column,
                 mutual_info_classif(
                     labels[column].to_frame(name=column),
                     labels[GlobalVariables.DatasetColumns.class_label],
                     discrete_features=True
                 )[0]]
            )

        colunas = []
        valores = []
        for value in numerical_discrete_m:
            if (int(value[1] * 100)) == 0:
                continue
            colunas.append(value[0])
            valores.append(int(value[1] * 100))

        aux = sort(colunas, valores)
        aux[0] = aux[0][:10]
        aux[1] = aux[1][:10]
        return aux

    @staticmethod
    def categorical(data, columns, class_label):
        categorical_m = []

        class_data = data[class_label]
        data.drop(columns=[class_label])
        for column in columns:
            true_label = class_data.__deepcopy__()
            pred_label = data[column]

            labels = pd.concat([true_label, pred_label], axis=1, sort=False)
            labels = labels.dropna()
            labels = labels.reset_index(drop=True)
            categorical_m.append(
                [column,
                 mutual_info_classif(
                     labels[column].to_frame(name=column),
                     labels[GlobalVariables.DatasetColumns.class_label]
                 )[0]]
            )

        colunas = []
        valores = []
        for value in categorical_m:
            if (int(value[1] * 100)) == 0:
                continue
            colunas.append(value[0])
            valores.append(int(value[1] * 100))

        aux = sort(colunas, valores)
        aux[0] = aux[0][:10]
        aux[1] = aux[1][:10]
        return aux

    @staticmethod
    def binary(data, columns, class_label):
        binary_m = []

        class_data = data[class_label]
        data.drop(columns=[class_label])
        for column in columns:
            true_label = class_data.__deepcopy__()
            pred_label = data[column]

            labels = pd.concat([true_label, pred_label], axis=1, sort=False)
            labels = labels.dropna()
            labels = labels.reset_index(drop=True)

            binary_m.append(
                [column,
                 mutual_info_classif(
                     labels[column].to_frame(name=column),
                     labels[GlobalVariables.DatasetColumns.class_label]
                 )[0]
                 ]
            )
        colunas = []
        valores = []
        for value in binary_m:
            if (int(value[1] * 100)) == 0:
                continue
            colunas.append(value[0])
            valores.append(int(value[1] * 100))

        aux = sort(colunas, valores)
        aux[0] = aux[0][:10]
        aux[1] = aux[1][:10]
        return aux

    @staticmethod
    def text(data, columns, class_label):
        text = []

        class_data = data[class_label]
        data.drop(columns=[class_label])
        for column in columns:
            true_label = class_data.__deepcopy__()
            pred_label = data[column]

            labels = pd.concat([true_label, pred_label], axis=1, sort=False)
            labels = labels.dropna()
            labels = labels.reset_index(drop=True)
            cv = CountVectorizer(max_df=0.95, min_df=2,
                                 max_features=10000)

            X_vec = cv.fit_transform(labels[column])

            dictionary = dict(zip(cv.get_feature_names(),
                                  mutual_info_classif(X_vec, labels[GlobalVariables.DatasetColumns.class_label],
                                                      discrete_features=True)
                                  ))
            colunas = []
            valores = []
            for col, val in dictionary.items():
                if (val * 100) == 0:
                    continue
                colunas.append(col)
                valores.append(val * 100)

            aux = sort(colunas, valores)
            aux[0] = aux[0][:10]
            aux[1] = aux[1][:10]
            text.append(aux)

        return text
