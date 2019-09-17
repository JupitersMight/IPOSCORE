import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.feature_extraction.text import CountVectorizer
from data.global_variables import GlobalVariables
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import os.path as path
from pathlib import Path


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

directory = Path(__file__).resolve().parents[2]
data = pd.read_csv(path.join(directory, 'data', r'data.csv'))

class_data = data[GlobalVariables.DatasetColumns.class_label]
data.drop(columns=[GlobalVariables.DatasetColumns.class_label])

BINARY_M = []
NUMERICAL_DISCRETE_M = []
CATEGORICAL_M = []
NUMERICAL_CONTINUOUS_M = []

for column in data.columns:
    true_label = class_data.__deepcopy__()
    pred_label = data[column]

    labels = pd.concat([true_label, pred_label], axis=1, sort=False)
    labels = labels.dropna()
    labels = labels.reset_index(drop=True)
    if column in GlobalVariables.DatasetColumns.ignored_columns:
        continue
    if column in GlobalVariables.DatasetColumns.text:
        print('')

        cv = CountVectorizer(max_df=0.95, min_df=2,
                            max_features=10000)

        X_vec = cv.fit_transform(labels[column])

        dictionary = dict(zip(cv.get_feature_names(),
                       mutual_info_classif(X_vec, labels[GlobalVariables.DatasetColumns.class_label], discrete_features=True)
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
        y_pos = np.arange(len(aux[0]))

        plt.barh(y_pos, aux[1], align='center', alpha=0.5)
        plt.yticks(y_pos, aux[0])
        plt.xlabel('Dependency (%)')
        plt.title(column)

        plt.savefig(column+'.png')
        plt.show()

    if column in GlobalVariables.DatasetColumns.binary:
        BINARY_M.append(
            [column,
             mutual_info_classif(
                 labels[column].to_frame(name=column),
                 labels[GlobalVariables.DatasetColumns.class_label]
             )[0]
             ]
        )
    elif column in GlobalVariables.DatasetColumns.categorical:
        CATEGORICAL_M.append(
            [column,
             mutual_info_classif(
                 labels[column].to_frame(name=column),
                 labels[GlobalVariables.DatasetColumns.class_label]
             )[0]]
        )
    elif column in GlobalVariables.DatasetColumns.numerical_discrete:
        NUMERICAL_DISCRETE_M.append(
            [column,
             mutual_info_classif(
                 labels[column].to_frame(name=column),
                 labels[GlobalVariables.DatasetColumns.class_label],
                 discrete_features=True
             )[0]]
        )
    elif column in GlobalVariables.DatasetColumns.numerical_continuous:
        NUMERICAL_CONTINUOUS_M.append(
            [column,
             mutual_info_regression(
                 labels[column].to_frame(name=column),
                 labels[GlobalVariables.DatasetColumns.class_label]
             )[0]]
        )
    else:
        for value in GlobalVariables.DatasetColumns.prefix_for_generated_columns:
            if value in column:
                BINARY_M.append(
                    [column, mutual_info_classif(
                        labels[column].to_frame(name=column),
                        labels[GlobalVariables.DatasetColumns.class_label]
                    )[0]]
                )
                break


colunas = []
valores = []
print('\n BINARY \n')
for value in BINARY_M:
    if (int(value[1]*100)) == 0:
        continue
    print('Column : '+value[0]+' mutual information: '+str(value[1])+'\n')
    colunas.append(value[0])
    valores.append(int(value[1]*100))

aux = sort(colunas, valores)
aux[0] = aux[0][:10]
aux[1] = aux[1][:10]
y_pos = np.arange(len(aux[0]))

plt.barh(y_pos, aux[1], align='center', alpha=0.5)
plt.yticks(y_pos, aux[0])
plt.xlabel('Dependency (%)')
plt.title('Binary Attributes')

plt.savefig('binary.png')
plt.show()


print('\n NUMERICAL_DISCRETE \n')
for value in NUMERICAL_DISCRETE_M:
    if (int(value[1]*100)) == 0:
        continue
    #print('Column : ' + value[0] + ' mutual information: ' + str(value[1]) + '\n')
    colunas.append(value[0])
    valores.append(int(value[1] * 100))

aux = sort(colunas, valores)
aux[0] = aux[0][:10]
aux[1] = aux[1][:10]
y_pos = np.arange(len(aux[0]))

plt.barh(y_pos, aux[1], align='center', alpha=0.5)
plt.yticks(y_pos, aux[0])
plt.xlabel('Dependency (%)')
plt.title('Numerical Discrete')

plt.savefig('discrite.png')
plt.show()


print('\n CATEGORICAL \n')
for value in CATEGORICAL_M:
    if (int(value[1]*100)) == 0:
        continue
    #print('Column : ' + value[0] + ' mutual information: ' + str(value[1]) + '\n')
    colunas.append(value[0])
    valores.append(int(value[1] * 100))

aux = sort(colunas, valores)
aux[0] = aux[0][:10]
aux[1] = aux[1][:10]
y_pos = np.arange(len(aux[0]))

plt.barh(y_pos, aux[1], align='center', alpha=0.5)
plt.yticks(y_pos, aux[0])
plt.xlabel('Dependency (%)')
plt.title('Categorical')

plt.savefig('categorical.png')
plt.show()

print('\n NUMERICAL_CONTINUOUS \n')
for value in NUMERICAL_CONTINUOUS_M:
    if (int(value[1]*100)) == 0:
        continue
    #print('Column : ' + value[0] + ' mutual information: ' + str(value[1]) + '\n')
    colunas.append(value[0])
    valores.append(int(value[1] * 100))

aux = sort(colunas, valores)
aux[0] = aux[0][:10]
aux[1] = aux[1][:10]
y_pos = np.arange(len(aux[0]))

plt.barh(y_pos, aux[1], align='center', alpha=0.5)
plt.yticks(y_pos, aux[0])
plt.xlabel('Dependency (%)')
plt.title('Numerical Continuous')

plt.savefig('continuous.png')
plt.show()

print('done')




