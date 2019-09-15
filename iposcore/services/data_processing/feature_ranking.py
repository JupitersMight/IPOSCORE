from data.global_variables import *
import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.feature_extraction.text import CountVectorizer


data = pd.read_csv(r'data.csv')

class_data = data[CLASS_LABEL]
data.drop(columns=[CLASS_LABEL])

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
    if column in IGNORE:
        continue
    if column in TEXT:
        print('')
        #Still Thinking on how to approach

        #cv = CountVectorizer(max_df=0.95, min_df=2,
                          #  max_features=10000)
        #X_vec = cv.fit_transform(labels[1])

        #print(dict(zip(cv.get_feature_names(),
                      # mutual_info_classif(X_vec, labels[0], discrete_features=True)
                      # )))
    if column in BINARY:
        BINARY_M.append([column, mutual_info_classif(labels[column].to_frame(name=column), labels[CLASS_LABEL])[0]])
    elif column in CATEGORICAL:
        CATEGORICAL_M.append([column, mutual_info_classif(labels[column].to_frame(name=column), labels[CLASS_LABEL])[0]])
    elif column in NUMERICAL_DISCRETE:
        NUMERICAL_DISCRETE_M.append([column, mutual_info_classif(labels[column].to_frame(name=column), labels[CLASS_LABEL], discrete_features=True)[0]])
    elif column in NUMERICAL_CONTINUOUS:
        NUMERICAL_CONTINUOUS_M.append([column, mutual_info_regression(labels[column].to_frame(name=column), labels[CLASS_LABEL])[0]])
    else:
        for value in PREFIXS:
            if value in column:
                BINARY_M.append([column, mutual_info_classif(labels[column].to_frame(name=column), labels[CLASS_LABEL])[0]])
                break



print('\n BINARY \n')
for value in BINARY_M:
    print('Column : '+value[0]+' mutual information: '+str(value[1])+'\n')

print('\n NUMERICAL_DISCRETE \n')
for value in NUMERICAL_DISCRETE_M:
    print('Column : ' + value[0] + ' mutual information: ' + str(value[1]) + '\n')

print('\n CATEGORICAL \n')
for value in CATEGORICAL_M:
    print('Column : ' + value[0] + ' mutual information: ' + str(value[1]) + '\n')

print('\n NUMERICAL_CONTINUOUS \n')
for value in NUMERICAL_CONTINUOUS_M:
    print('Column : ' + value[0] + ' mutual information: ' + str(value[1]) + '\n')








