from utils import *


# DF de presença
df_Redacao = pd.read_csv("C:\Projetos Pessoais\DataScience\/0_dados_pesados\data\MICRODADOS_ENEM_2021.csv", sep= ";", encoding="ISO-8859-1", usecols=col_redacao)

# Criação coluna eliminados, para todos os candidatos, com base em isna() em cada prova
df_Redacao['ELIMINADOS_CONC'] = np.where(df_Redacao['TP_STATUS_REDACAO'].isna(), 'Eliminado', 'Presente') 

print(df_Redacao.columns)
print(df_Redacao.isna().sum())
print(df_Redacao)

# Panorama redação por tipo/ escola - com todas as competências
nota_porTipoEscola = df_Redacao[df_Redacao['ELIMINADOS_CONC'] == 'Presente']\
                  .loc[df_Redacao['TP_ESCOLA'].isin([2,3])]\
                  .groupby('TP_ESCOLA')['NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3',
       'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO']\
                  .agg(['mean'])

print(nota_porTipoEscola)

# Panorama média/geral por competencias

media_porCompetencia = df_Redacao[df_Redacao['ELIMINADOS_CONC'] == 'Presente']\
                   .groupby(['ELIMINADOS_CONC'])['NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3',
       'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO'].agg(['mean']).reset_index()

print(media_porCompetencia)

# panorama de status da redação 

status_redacao = df_Redacao[df_Redacao['ELIMINADOS_CONC'] == 'Presente']\
                  .loc[df_Redacao['TP_ESCOLA'].isin([2,3])]\
                  .groupby(['TP_ESCOLA', 'TP_STATUS_REDACAO'])['TP_STATUS_REDACAO']\
                  .agg(['count']).rename(columns={'count': 'Quantidade'}).reset_index()
status_redacao['TP_ESCOLA'] = status_redacao['TP_ESCOLA'].replace(mapeamento_por_tipoEscola)
status_redacao['TP_STATUS_REDACAO'] = status_redacao['TP_STATUS_REDACAO'].replace(mapeamento_status_redacao)
''' Gerar 3 DF - 1 com informações de redações "OK 
e outro com info das redações anuladas
e total"'''

status_redacao_anuladas = status_redacao.loc[status_redacao['TP_STATUS_REDACAO']\
                                             .isin(['Anulada', 'Cópia Texto Motivador', 'Em Branco',
                                                     'Fuga ao Tema','Tipo Texto Incorreto', 'Texto Insuficiente', 'Parte Desconectada'])]

status_redacao_OK = status_redacao.loc[status_redacao['TP_STATUS_REDACAO']\
                                             .isin(['Sem Problemas'])]

status_redacao_total = status_redacao.groupby('TP_ESCOLA')['Quantidade'].sum().reset_index()

print(status_redacao)
print(status_redacao_anuladas)
print(status_redacao_OK)
print(status_redacao_total)



#Panorama geral das notas
df_filtrado = df_Redacao[df_Redacao['NU_NOTA_REDACAO'].notna()]
df_nota_histograma = df_filtrado[['NU_INSCRICAO', 'NU_NOTA_REDACAO']]

print(df_nota_histograma.head())  

'''
PLOTAGEM
'''


"""HISTPLOT MÉDIA GERAL DA REDAÇÃO COM A QUANTIDADE DE PESSOAS"""

# sns.set()
# sns.histplot(data=df_nota_histograma, x='NU_NOTA_REDACAO',color="#ed6044",
#               bins=50, kde=True)
# # Configurações adicionais
# plt.xlabel('Nota Média')
# plt.ylabel('Quantidade de candidatos')
# plt.title('Densidade da Nota Média / Redação')

# plt.yticks(color = 'grey')
# plt.xticks(range(0, 1001, 50), color='grey', fontsize = 9,
#            rotation = 40)
# plt.show()



""" STATUS REDAÇÃO ANULADAS / OK / QTDE """
cores3 = sns.set_palette("OrRd")
plt.figure(figsize=(12, 6))
# Desenhar o gráfico de pizza com as quantidades
wedges, texts, autotexts = plt.pie(status_redacao_total['Quantidade'], labels=status_redacao_total['TP_ESCOLA'],
                                   autopct='%1.1f%%', startangle=143,colors=cores3)
# Configurar as propriedades dos textos
plt.setp(autotexts, size=12, color='black')
# Limpar o círculo central
centre_circle = plt.Circle((0, 0), 0.85, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
# Calcular e exibir a quantidade total
total = status_redacao_total['Quantidade'].sum()
plt.text(0, -0.4, 'Candidatos Presentes: {}'.format(total), ha='center', va='center', fontsize=10)
plt.title('Panorama de Candidatos de Escola Pública e Particular', y = 1.01)
plt.show()

    
# # Gráfico Lineplot
# fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

# sns.lineplot(data=df_publica, x='TP_STATUS_REDACAO', y='Quantidade', ax=ax1, label='Pública')
# sns.lineplot(data=df_privada, x='TP_STATUS_REDACAO', y='Quantidade', ax=ax1, label='Privada')

# ax1.set_xlabel('Status da Redação')
# ax1.set_ylabel('Quantidade')
# ax1.set_title('Distribuição por Status da Redação')
# ax1.legend()

# # Gráfico de Pizza
# contagem_sem_problemas_publica = df_publica[df_publica['TP_STATUS_REDACAO'] == 'Sem Problemas']['Quantidade'].iloc[0]
# contagem_sem_problemas_privada = df_privada[df_privada['TP_STATUS_REDACAO'] == 'Sem Problemas']['Quantidade'].iloc[0]

# contagem_sem_problemas = [contagem_sem_problemas_publica, contagem_sem_problemas_privada]
# labels = ['Pública', 'Privada']

# ax2.pie(contagem_sem_problemas, labels=labels, autopct='%1.1f%%', startangle=90)
# ax2.set_title('Quantidade de "Sem Problemas"')

# # Ajustar o layout
# plt.tight_layout()

# # Exibir a plotagem
# plt.show()




# # Transformar as colunas em linhas utilizando o melt
# df_melted = nota_internet.melt(id_vars='Q025', var_name='Nota', value_name='Valor')
# # Plotar o gráfico de linhas
# g = sns.lineplot(
#     data=df_melted, x='Nota', y='Valor', hue='Q025',
#     palette='Set2', markers=True, style='Q025'
# )
# for _, row in df_melted.iterrows():
#     g.annotate(round(row['Valor'], 2), (row['Nota'], row['Valor']),
#                textcoords="offset points",fontsize=8, xytext=(0,10), ha='center')

# plt.xticks(rotation=20, fontsize = 9, color = 'grey')
# plt.yticks(fontsize = 9, color = 'grey')
# plt.ylabel('Nota Média')
# plt.xlabel('Matérias')
# # # Borda top e right invisiveis
# g.spines['top'].set_visible(False)
# g.spines['right'].set_visible(False)
# g.spines['left'].set_visible(False)

# #Grid
# g.yaxis.grid(True, alpha=0.1)
# g.set_axisbelow(True)
# plt.ylim(400, 700)
# g.set_xlabel(g.get_xlabel(), fontweight='bold')
# g.set_ylabel(g.get_ylabel(), fontweight='bold')
# plt.title('Desempenho com base no acesso à internet', y = 1.03)
# plt.legend(bbox_to_anchor=(1.05, 0.5), loc='center left')
# plt.show()
