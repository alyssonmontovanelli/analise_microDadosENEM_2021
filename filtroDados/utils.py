import pandas as pd
import numpy as np

#panorama presença/faltas por região/sexo/raça
colPresenca = ['NU_INSCRICAO', 'TP_SEXO', 'TP_COR_RACA',
                   'SG_UF_PROVA', 'TP_PRESENCA_MT', 'TP_PRESENCA_LC']

#panorama tipo de escola / nota final / redação
colEscola_nota = ['NU_INSCRICAO', 'TP_ESCOLA', 'SG_UF_PROVA', 'NU_NOTA_CN',
                  'NU_NOTA_LC', 'NU_NOTA_CH', 'NU_NOTA_MT',
                  'NU_NOTA_REDACAO']

#panorama das principais dificuldades na prova de redação para alunos\
#de rede publica e privada
col_redacao = ['TP_ESCOLA', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1',
               'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4',
               'NU_NOTA_COMP5']