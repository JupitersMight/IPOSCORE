import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.feature_extraction.text import CountVectorizer
from data.global_variables import GlobalVariables


data = pd.read_csv(r'data.csv')

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
        #Still Thinking on how to approach

        #cv = CountVectorizer(max_df=0.95, min_df=2,
                          #  max_features=10000)
        #X_vec = cv.fit_transform(labels[1])

        #print(dict(zip(cv.get_feature_names(),
                      # mutual_info_classif(X_vec, labels[0], discrete_features=True)
                      # )))
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








