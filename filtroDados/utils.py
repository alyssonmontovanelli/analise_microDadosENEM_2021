import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

#panorama presença/faltas por região/sexo/raça
colPresenca = ['NU_INSCRICAO', 'TP_SEXO', 'TP_COR_RACA',
                   'SG_UF_PROVA', 'TP_PRESENCA_MT', 'TP_PRESENCA_LC']

#panorama tipo de escola / nota final / redação
colEscola_nota = ['NU_INSCRICAO', 'TP_COR_RACA' , 'TP_ESCOLA', 'SG_UF_PROVA', 'NU_NOTA_CN',
                  'NU_NOTA_LC', 'NU_NOTA_CH', 'NU_NOTA_MT',
                  'NU_NOTA_REDACAO']

#panorama das principais dificuldades na prova de redação para alunos\
#de rede publica e privada
col_redacao = ['NU_INSCRICAO','TP_COR_RACA', 'TP_ESCOLA', 'SG_UF_PROVA', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1',
               'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4',
               'NU_NOTA_COMP5','NU_NOTA_REDACAO']


col_socioEconomico = ['NU_INSCRICAO', 'TP_COR_RACA', 'TP_ESCOLA','SG_UF_PROVA','NU_NOTA_CN',
                  'NU_NOTA_LC', 'NU_NOTA_CH', 'NU_NOTA_MT',
                  'NU_NOTA_REDACAO','Q001', 'Q002','Q003','Q004','Q005', 'Q006', 'Q025']


# sns.color_palette("Spectral", as_cmap=True)

''' MAPEAMENTO COM BIBLIOTECAS, PARA CONVERSÃO DE MICRO DADO '''
mapeamento_por_tipoEscola = {
    1: 'Não informado',
    2: 'Pública',
    3: 'Privada'
}
mapeamento_cor_raca = {
    0: 'Não declarado',
    1: 'Branco',
    2: 'Preto',
    3: 'Pardo',
    4: 'Amarelo',
    5: 'Indígena'
}
mapeamento_nota_materia = {
    'NU_NOTA_CN': 'Ciências da Natureza',
    'NU_NOTA_LC': 'Linguagens e Códigos',
    'NU_NOTA_CH': 'Ciências Humanas',
    'NU_NOTA_MT': 'Matemática',
    'NU_NOTA_REDACAO': 'Redação',
    'MEDIA_GERAL': 'Média Geral'
}
mapeamento_renda = {
    'A': 'Nenhuma Renda',
    'B': 'Até 1.100,00',
    'C': '1.100,01 - 1650,00',
    'D': '1650,01 - 2.200,00',
    'E': '2.200,01 - 2.750,00',
    'F': '2.750,01 - 3.300,00',
    'G': '3.300,01 - 4.400,00',
    'H': '4.400,01 - 5.500,00',
    'I': '5.500,01 - 6.600,00',
    'J': '6.600,01 - 7.700,00',
    'K': '7.700,01 - 8.800,00',
    'L': '8.800,01 - 9.900,00',
    'M': '9.900,01 - 11.000,00',
    'N': '11.000,01 - 13.200,00',
    'O': '13.200,01 - 16.500,00',
    'P': '16.500,01 - 22.000,00',
    'Q': 'Acima de 22.000,00',
}
mapeamento_internet = {
    'A': 'Sem acesso',
    'B': 'Com acesso'
}

mapeamento_ocupacao = {
    'A': 'Grupo 1',
    'B': 'Grupo 2',
    'C': 'Grupo 3',
    'D': 'Grupo 4',
    'E': 'Grupo 5',
    'F': 'Sem resposta',
}

mapeamento_escolaridade_responsavel = {
    'A': 'Nunca estudou',
    'B': '5º Ano incompleto',
    'C': '5º ano Completou',
    'D': 'E.F completo',
    'E': 'E.M completo',
    'F': 'E.S completo',
    'G': 'Pós-graduação',
    'H': 'Sem resposta'
}
