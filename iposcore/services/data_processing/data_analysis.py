import pandas as pd
from services.data_processing.utils import Utils


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


missings = Utils.number_of_missing_values(data)
i=0
for value in missings:
    percentage = value*100/len(data['complicação pós-cirúrgica'])
    if(percentage > 70):
        file.write('Attribute '+str(final_columns[i]+': '+str(percentage)+' missing values \n'))
    i+=1


file.write('\n')

for column in data.columns:
    d = Utils.distribution(data[column])
    for i in range(len(d)):
        total = 0
        for j in range(len(d)):
            total += d[j].counter
        percentage = d[i].counter*100/total
        if(percentage > 70):
            file.write('Attribute \"' + str(column) + '\" contains ' + str(percentage) + ' of value ' + str(d[i].name) + '\n')



file.close()

print('done')


























