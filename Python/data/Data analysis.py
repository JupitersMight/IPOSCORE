import numpy as np
import pandas as pd
import math
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing
from scipy.stats import sem, t


class data_column:
    def __init__(self, name, age):
        self.name = name
        self.counter = age


def preprocess_substitute_na_with_average(dataset):
    list_of_columns = dataset.columns
    array_of_mean_values = []
    for column_name in list_of_columns:
        if column_name == "class":
            continue
        list_of_items = dataset[column_name]

        array_of_mean_values.append(calculate_mean_with_na(list_of_items))

    i = 0

    for column_name in list_of_columns:
        if column_name == "class":
            continue
        dataset[column_name].fillna(str(array_of_mean_values[i]))
        i += 1


def calculate_mean_with_na(list):
    sum_value = 0
    counter = 0
    for value in list:
        if value != "na":
            if isinstance(value, str):
                value = float(value)
            sum_value = sum_value + value
            counter += 1
    return sum_value/counter


def calculate_mean(dataset):
    mean_values = []
    for column_name in dataset.columns:
        if column_name == "class":
            continue
        sum_values = 0
        i = 0
        for value in dataset[column_name]:
            if value == 'n/a':
                continue
            sum_values += float(value)
            i += 1
        mean_values.append(str(sum_values/i))
    return mean_values


def distribution(column):
    different_values = []
    for value in column:
        if(value == 'n/a'):
            continue
        isInArray = False
        for i in range(len(different_values)):
            if(value == different_values[i].name):
                isInArray = True
                different_values[i].counter += 1
                break
        if(not isInArray):
            different_values.append(data_column(value, 1))
    return different_values


def number_of_missing_values(dataset):
    missing_values = []
    for column_name in dataset.columns:
        counter = 0
        for value in dataset[column_name]:
            if value != 'n/a':
                continue
            counter += 1
        missing_values.append(counter)
    return missing_values


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


def draw_heatmap_of_features(dataset, X, y, filename):
    selector = SelectKBest(chi2, k=4)
    X_new = selector.fit_transform(X, y)
    # Get idxs of columns to keep
    idxs_selected = selector.get_support(indices=True)
    columns = []
    for idx in idxs_selected:
        columns.append(dataset.columns[idx])
    X_new = pd.DataFrame(data=X_new, columns=columns)

    corr = X_new.corr()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0, len(X_new.columns), 1)
    ax.set_xticks(ticks)
    plt.xticks(rotation=90)
    ax.set_yticks(ticks)
    ax.set_xticklabels(X_new.columns)
    ax.set_yticklabels(X_new.columns)
    plt.savefig(filename, dpi=100)
    plt.show()


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
        if max_value-min_value > 0:
            result.append((float(value) - min_value) / (max_value - min_value))

    return result


#################################### All Data ####################################


data = pd.read_csv(r'data.csv', dtype=str)
final_columns = []

for column in data.columns:
    final_columns.append(column)
    data[column] = data[column].fillna('n/a')


file = open('statistics.txt', 'w')
file.write('Number of attributes : '+str(len(data.columns))+' | Number of rows : '+str(len(data['complicação pós-cirúrgica']))+'\n')
#Complicações
file.write('There are '+str(len(data[data['complicação pós-cirúrgica'] == '1']))+ ' patients with complications post cirurgy \n')
file.write('There are '+str(len(data[data['complicação pós-cirúrgica'] == '0']))+ ' patients without complications post cirurgy \n\n')
#Quimio
quimio = data[data['QT pré-operatória'] == '1']
semQuimio = data[data['QT pré-operatória'] == '0']
file.write('There are '+str(len(quimio[quimio['complicação pós-cirúrgica'] == '1']))+ ' patients with post cirurgy complications that had pre operation quimio \n')
file.write('There are '+str(len(quimio[quimio['complicação pós-cirúrgica'] == '0']))+ ' patients without post cirurgy complications that had pre operation quimio \n')
file.write('There are '+str(len(semQuimio[semQuimio['complicação pós-cirúrgica'] == '1']))+ ' patients with post cirurgy complications that did not have pre operation quimio \n')
file.write('There are '+str(len(semQuimio[semQuimio['complicação pós-cirúrgica'] == '0']))+ ' patients without post cirurgy complications that did not have pre operation quimio \n\n')
#Primeira cirugia
primeira = data[data['1ª Cirurgia IPO'] == '1']
naoprimeira = data[data['1ª Cirurgia IPO'] == '0']
file.write('There are '+str(len(primeira[primeira['complicação pós-cirúrgica'] == '1']))+ ' patients with post cirurgy complications that were operated by the first time \n')
file.write('There are '+str(len(primeira[primeira['complicação pós-cirúrgica'] == '0']))+ ' patients without post cirurgy complications that were operated by the first time \n')
file.write('There are '+str(len(naoprimeira[naoprimeira['complicação pós-cirúrgica'] == '1']))+ ' patients with post cirurgy complications that were not operated by the first time \n')
file.write('There are '+str(len(naoprimeira[naoprimeira['complicação pós-cirúrgica'] == '0']))+ ' patients without post cirurgy complications that were not operated by the first time \n\n')
#Cirugia urgente ou não
cirugiaUrgente = data[data['tipo cirurgia'] == '2']
cirugiaNaoUrgente = data[data['tipo cirurgia'] == '1']
file.write('There are '+str(len(cirugiaUrgente[cirugiaUrgente['complicação pós-cirúrgica'] == '1'])) + ' (complications sim, cirurgia urgente sim) \n')
file.write('There are '+str(len(cirugiaUrgente[cirugiaUrgente['complicação pós-cirúrgica'] == '0'])) + ' (complications não, cirurgia urgente sim) \n')
file.write('There are '+str(len(cirugiaNaoUrgente[cirugiaNaoUrgente['complicação pós-cirúrgica'] == '1'])) + ' (complications sim, cirurgia urgente não) \n')
file.write('There are '+str(len(cirugiaNaoUrgente[cirugiaNaoUrgente['complicação pós-cirúrgica'] == '0'])) + ' (complications não, cirurgia urgente não) \n\n')
#Tipo de cirurgia
toracica = data[data['especialidade_COD'] == '1']
digestivo = data[data['especialidade_COD'] == '2']
orl = data[data['especialidade_COD'] == '3']
outra = data[data['especialidade_COD'] == '4']
file.write('There are '+str(len(toracica[toracica['complicação pós-cirúrgica'] == '1']))+ ' patients with post cirurgy complications (toracica) \n')
file.write('There are '+str(len(toracica[toracica['complicação pós-cirúrgica'] == '0']))+ ' patients without post cirurgy complications (toracica) \n')
file.write('There are '+str(len(digestivo[digestivo['complicação pós-cirúrgica'] == '0']))+ ' patients without post cirurgy complications (digestivo) \n')
file.write('There are '+str(len(digestivo[digestivo['complicação pós-cirúrgica'] == '1']))+ ' patients with post cirurgy complications (digestivo) \n')
file.write('There are '+str(len(orl[orl['complicação pós-cirúrgica'] == '1']))+ ' patients with post cirurgy complications (cabeça) \n')
file.write('There are '+str(len(orl[orl['complicação pós-cirúrgica'] == '0']))+ ' patients without post cirurgy complications (cabeça) \n')
file.write('There are '+str(len(outra[outra['complicação pós-cirúrgica'] == '1']))+ ' patients with post cirurgy complications (outra) \n')
file.write('There are '+str(len(outra[outra['complicação pós-cirúrgica'] == '0']))+ ' patients without post cirurgy complications (outra) \n\n')
#Morreu no primeiro ano
obito1 = data[data['óbito até 1 ano '] == '1']
obito0 = data[data['óbito até 1 ano '] == '0']
file.write('There are '+str(len(obito1[obito1['complicação pós-cirúrgica'] == '1']))+ ' patients with post cirurgy complications that died on the first year \n')
file.write('There are '+str(len(obito1[obito1['complicação pós-cirúrgica'] == '0']))+ ' patients without post cirurgy complications that died on the first year \n')
file.write('There are '+str(len(obito0[obito0['complicação pós-cirúrgica'] == '1']))+ ' patients with post cirurgy complications that didn\'t die on the first year \n')
file.write('There are '+str(len(obito0[obito0['complicação pós-cirúrgica'] == '0']))+ ' patients without post cirurgy complications that didn\'t die on the first year \n\n')
#Reinternamento
reinternamento = data[data[' reinternamento na UCI'] == '1']
reinternamentoN = data[data[' reinternamento na UCI'] == '0']
file.write('There are '+str(len(reinternamento[reinternamento['complicação pós-cirúrgica'] == '1']))+ ' patients with post cirurgy complications (reinternamento na UCI) \n')
file.write('There are '+str(len(reinternamento[reinternamento['complicação pós-cirúrgica'] == '0']))+ ' patients without post cirurgy complications (reinternamento na UCI) \n')
file.write('There are '+str(len(reinternamentoN[reinternamentoN['complicação pós-cirúrgica'] == '1']))+ ' patients with post cirurgy complications (não reinternamento na UCI) \n')
file.write('There are '+str(len(reinternamentoN[reinternamentoN['complicação pós-cirúrgica'] == '0']))+ ' patients without post cirurgy complications (não reinternamento na UCI) \n\n')


missings = number_of_missing_values(data)
i=0
for value in missings:
    percentage = value*100/len(data['complicação pós-cirúrgica'])
    if(percentage > 70):
        file.write('Attribute '+str(final_columns[i]+': '+str(percentage)+' missing values \n'))
    i+=1


file.write('\n')

for column in data.columns:
    d = distribution(data[column])
    for i in range(len(d)):
        total = 0
        for j in range(len(d)):
            total += d[j].counter
        percentage = d[i].counter*100/total
        if(percentage > 70):
            file.write('Attribute \"' + str(column) + '\" contains ' + str(percentage) + ' of value ' + str(d[i].name) + '\n')



file.close()

print('done')


























