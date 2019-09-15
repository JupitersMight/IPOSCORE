
class GlobalVariables:

    class DatabaseConfigurations:
        user = 'postgres'
        password = ''
        host = '127.0.0.1'
        port = '5432'
        database = 'test'

    class DatasetColumns:
        class_label = 'complicação pós-cirúrgica'

        numerical_continuous = ['dias na UCI',
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
                                   ] #35

        categorical = ['tipo pedido anestesia',
                        'proveniência',
                        'motivo admissão UCI',
                        'tipo cirurgia',
                        'especialidade_COD',
                        'destino após UCI',
                        'ASA',
                        'PP idade',
                        'PP cardíaco',
                        'PP respiratório',
                        'PP ECG',
                        'PP pressão arterial sistólica',
                        'PP pulsação arterial',
                        'PP hemoglobina',
                        'PP leucócitos',
                        'PP ureia',
                        'PP sódio',
                        'PP potássio',
                        'PP escala glasglow',
                        'PP tipo operação',
                        'PP nº procedimentos',
                        'PP perda sangue',
                        'PP contaminação peritoneal',
                        'PP estado da malignidade',
                        'PP CEPOD-classificação operação',
                        'ACS idade',
                        'ACS estado funcional',
                        'ACS ASA',
                        'ACS sépsis sistémica',
                        'ACS diabetes',
                        'ACS dispneia',
                        'ARISCAT Idade',
                        'ARISCAT SpO2 ',
                        'ARISCAT incisão cirúrgica',
                        'ARISCAT duração cirurgia',
                        'SCORE ARISCAT',
                        'CHARLSON Idade',
                        'CHARLSON Diabetes mellitus',
                        'CHARLSON Doença fígado',
                        'CHARLSON Malignidade',
                        'complicação principal_COD',
                        'classificação ACS complicações gerais',
                        'classificação clavien-dindo',
                        'destino após IPO',
                        'óbito_tempo decorrido após data cirurgia (até 1 ano)'
                        ]#45

        numerical_discrete = ['idade',
                              'dias no  IPOP',
                              'Score fisiológico P-Possum',
                              'Score gravidade cirúrgica P-Possum',
                              'ACS altura',
                              'ARISCAT PONTUAÇÃO TOTAL',
                              'PONTOS - Charlson Comorbidity Index',
                              '% Sobrevida estimada em 10 anos'
                              ]#8

        binary = ['1ª Cirurgia IPO',
                    'QT pré-operatória',
                    ' reinternamento na UCI',
                    'género',
                    'ACS género',
                    'ACS emergência',
                    'ACS esteróides',
                    'ACS ascite',
                    'ACS dependente ventilador',
                    'ACS cancro disseminado',
                    'ACS hipertensão',
                    'ACS ICC',
                    'ACS fumador',
                    'ACS DPOC',
                    'ACS diálise',
                    'ACS insuficiência renal aguda',
                    'ARISCAT infeção respiratória último mês',
                    'ARISCAT anemia pré-operativa',
                    'ARISCAT procedimento emergente',
                    'CHARLSON SIDA',
                    'CHARLSON Doença Renal Crónica Moderada a Severa',
                    'CHARLSON Insuficiência Cardíaca',
                    'CHARLSON Enfarte Miocárdio',
                    'CHARLSON DPOC',
                    'CHARLSON Doença Vascular periférica',
                    'CHARLSON AVC ou Ataque Isquémico Transitório',
                    'CHARLSON Demência',
                    'CHARLSON Hemiplegia',
                    'CHARLSON Doença do Tecido Conjuntivo',
                    'CHARLSON Úlcera Péptica',
                    'óbito até 1 ano '
                  ]#32

        text = ['especialidade',
                'LOCALIZAÇÃO ',
                'diagnóstico pré-operatório',
                'Operação efetuada',
                'procedimentos_COD',
                'descrição complicação pós-cirúrgica',
                'complicação_COD',
                'Informação adicional',
                'Comorbilidades pré-operatórias'
                ]#9

        dates = ['data pedido pela anestesia',
                'data admissão UCI',
                'data cirurgia',
                'data óbito'
                ]#4

        ignored_columns = ['Intervenções_ICD10',
                           'ACS_procedimento',
                           'nº IPO', 'classificação ACS complicações específicas'
                           ]#4

        prefix_for_generated_columns = ['ACS_',
                                        'ICD_',
                                        'ACS_CE_'
                                        ]#3
