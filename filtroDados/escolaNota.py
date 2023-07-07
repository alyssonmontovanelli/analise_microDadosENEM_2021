from utils import *

df_notaEscola = pd.read_csv("C:\Projetos Pessoais\DataScience\/0_dados_pesados\data\MICRODADOS_ENEM_2021.csv",\
                             sep= ";", encoding="ISO-8859-1", usecols=colEscola_nota)

# Criação coluna eliminados, para todos os candidatos, com base em isna() em cada prova
df_notaEscola['ELIMINADOS_CONC'] = np.where((df_notaEscola['NU_NOTA_CN'].isna())\
                                         | (df_notaEscola['NU_NOTA_CH'].isna())\
                                         | (df_notaEscola['NU_NOTA_LC'].isna())\
                                         | (df_notaEscola['NU_NOTA_MT'].isna())\
                                         | (df_notaEscola['NU_NOTA_REDACAO'].isna()), 'Eliminado', 'Presente')

# Criação de coluna media geral dos alunos presentes nos dois dias de prova
df_notaEscola.loc[df_notaEscola['ELIMINADOS_CONC'] == 'Presente', 'MEDIA_GERAL']\
   = df_notaEscola[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean(axis=1)

# Média geral/UF - proporcional com a população
media_UF = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente'].groupby('SG_UF_PROVA')['MEDIA_GERAL'].mean().reset_index()

# Média geral para alunos brancos e negros
media_raca = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente']\
            .loc[df_notaEscola['TP_COR_RACA'].isin([1,2,3,4,5])]\
            .groupby('TP_COR_RACA')['MEDIA_GERAL']\
            .agg(['mean','count']).reset_index()\
            .rename(columns={'TP_COR_RACA':'Cor/Raça','mean': 'Nota Média', 'count': 'Quantidade'})

# Mapear os valores da coluna 'Cor/Raça' para os novos nomes

media_raca['Cor/Raça'] = media_raca['Cor/Raça'].replace(mapeamento_cor_raca)

# Quantidade de alunos negros, brancos e pardos em escola publica/privada

raca_porEscola = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente']\
                 .loc[df_notaEscola['TP_COR_RACA'].isin([1,2,3])]\
                 .groupby(['TP_ESCOLA', 'TP_COR_RACA'])\
                .size() \
                 .reset_index(name='Quantidade')

raca_porEscola['TP_COR_RACA'] = raca_porEscola['TP_COR_RACA'].replace(mapeamento_cor_raca)
raca_porEscola['TP_ESCOLA'] = raca_porEscola['TP_ESCOLA'].replace(mapeamento_por_tipoEscola)

# Inscritos por tipo/escola que faltaram ou estava presentes 
inscritos_presentes = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente']\
                 .loc[df_notaEscola['TP_COR_RACA'].isin([1,2,3])]\
                 .groupby(['TP_ESCOLA', 'TP_COR_RACA'])['TP_COR_RACA'].count()



# Panorama tipo_escola com média geral
media_tipoEscola = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente']\
                  .loc[df_notaEscola['TP_ESCOLA'].isin([2,3])]\
                  .groupby(['TP_ESCOLA'])['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT','NU_NOTA_REDACAO','MEDIA_GERAL']\
                  .agg(['mean']).reset_index()
media_tipoEscola['TP_ESCOLA'] = media_tipoEscola['TP_ESCOLA'].replace(mapeamento_por_tipoEscola)
media_tipoEscola.rename(columns=mapeamento_nota_materia, inplace=True)

# Panorama tipo_escola por UF - média de notas 

media_tipoEscola_porUF = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente']\
                  .loc[df_notaEscola['TP_ESCOLA'].isin([1,2,3])]\
                  .groupby('SG_UF_PROVA')['MEDIA_GERAL']\
                  .mean()\
                 .reset_index(name='Média')
media_tipoEscola_porUF.rename(columns={'SG_UF_PROVA': 'Sigla UF'}, inplace=True)

media_tipoEscola_porUF = media_tipoEscola_porUF.sort_values(by='Média', ascending=False)



df_filtrado_geral = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente']
df_notaGeral_histograma = df_notaEscola[['NU_INSCRICAO', 'MEDIA_GERAL']]







'''
PLOTAGEM
'''




cores2 = sns.color_palette("OrRd")
media_raca_sorted = media_raca.sort_values('Cor/Raça')

""" HistPlot - MÉDIA DE NOTA GERAL POR PRESENTES """
sns.set()
sns.histplot(data=df_notaGeral_histograma, x='MEDIA_GERAL',color="#ed6044",
              bins=50, kde=True)
# Configurações adicionais
plt.xlabel('Nota Média (pontos)')
plt.ylabel('Quantidade de candidatos')
plt.title('Densidade da Nota Média')

plt.yticks(color = 'grey')
plt.xticks(range(0, 900, 50), color='grey', fontsize = 9,
           rotation = 40)


plt.show()


""" Barplot - média por raça--------------------------------------------------------"""
# plt.figure(figsize=(10, 6))

# # Adicionar os valores das barras no gráfico
# ax = sns.barplot(x='Cor/Raça', y='Nota Média', data=media_raca_sorted, palette='OrRd')
# for p in ax.patches:
#     ax.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
# # Ajustar a estética do gráfico
# sns.set(style='whitegrid')
# plt.title('Média de Nota Por Cor/Raça', y=1.03)
# plt.xlabel('Cor/Raça', fontsize = 12)
# plt.ylabel('Nota Média', fontsize = 12)
# plt.xticks(rotation = 20, color='grey', fontsize = 10)
# plt.yticks(color='grey', fontsize = 10)
# # Mostrar os grids
# ax.yaxis.grid(True, color='lightgrey')
# ax.set_axisbelow(True)
# # Borda top e right invisiveis
# ax.spines['top'].set_visible(False)
# ax.spines['left'].set_visible(False)
# ax.spines['right'].set_visible(False)
# # Mostrar o gráfico
# plt.show()


""" Pie - Qtde por raça ------------------------------------------------------------------"""
# plt.figure(figsize=(12, 6))
# # Desenhar o gráfico de pizza com as quantidades
# wedges, texts, autotexts = plt.pie(media_raca_sorted['Quantidade'], labels=media_raca_sorted['Cor/Raça'],
#                                    autopct='%1.1f%%', startangle=100,colors=cores2)
# # Configurar as propriedades dos textos
# plt.setp(autotexts, size=10, color='black')

# # for label, wedge in zip(texts, wedges):
# #     label.set_color(wedge.get_facecolor())
# #     label.set_fontweight('bold')
# #     label.set_fontsize(10)  # Adicionar formatação em negrito


# # Limpar o círculo central
# centre_circle = plt.Circle((0, 0), 0.85, fc='white')
# fig = plt.gcf()
# fig.gca().add_artist(centre_circle)
# # Calcular e exibir a quantidade total
# total = media_raca['Quantidade'].sum()
# plt.text(0, -0.4, 'Total: {}'.format(total), ha='center', va='center',color = '#f77e52', fontsize = 12,fontweight='bold')
# plt.title('Inscritos Presentes Por Cor/Raça Declarada', y=1.03)
# plt.show()


""" CATPLOT - TP ESCOLA / RAÇA/ QUANTIDADE -------------------------------------------"""



# g = sns.catplot(
#     data=raca_porEscola, kind="bar",
#     x="TP_ESCOLA", y="Quantidade", hue="TP_COR_RACA",
#     errorbar="sd",palette='OrRd', height=6
# )
# ax = g.facet_axis(0, 0)
# for p in ax.patches:
#     ax.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()),\
#                  ha='center', va='center', xytext=(0, 9),rotation=20, fontsize=8, color = 'grey', textcoords='offset points')

# g.despine(left=True)
# g.set_axis_labels("Tipo da Escola", "Qtde candidatos")
# plt.xticks(color = 'grey', rotation = 20)
# plt.yticks(color = 'grey')

# g.legend.set_title("Cor/Raça")
# plt.title("Distribuição dos candidatos Pela Cor e Tipo de Escola", y= 1.03)
# plt.show()



""" LINEPLOT - NOTA MÉDIA POR TIPO DE ESCOLA -------------------------------------------"""
# # Transformar as colunas em linhas utilizando o melt
# df_melted = media_tipoEscola.melt(id_vars='TP_ESCOLA', var_name='Nota', value_name='Valor')
# # Plotar o gráfico de linhas
# g = sns.lineplot(
#     data=df_melted, x='Nota', y='Valor', hue='TP_ESCOLA',
#     palette='OrRd', markers=True, style='TP_ESCOLA'
# )
# for _, row in df_melted.iterrows():
#     g.annotate(round(row['Valor'], 2), (row['Nota'], row['Valor']),
#                textcoords="offset points",fontsize=8, color = 'grey', xytext=(0,10), ha='center')
    
# plt.xticks(rotation=20, fontsize = 9, color = 'grey')
# plt.yticks(fontsize = 9, color = 'grey')
# plt.ylabel('Nota Média')
# plt.xlabel('Matérias')
# # # Borda top e right invisiveis
# g.spines['top'].set_visible(False)
# g.spines['right'].set_visible(False)
# g.spines['left'].set_visible(False)

# #Grid
# g.yaxis.grid(color='lightgrey', alpha=0.5)
# g.set_axisbelow(True)
# plt.ylim(400, 800)
# plt.title('Nota Média por Tipo de Escola', y = 1.03, fontweight='bold')
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.show()

""" BARPLOT - NOTA MÉDIA POR UF -------------------------------------------"""

# plt.figure(figsize=(12, 6))
# # sns.barplot(x='Sigla UF', y='Média', data=media_tipoEscola_porUF)
# # sns.set_palette(cores2)
# # Adicionar os valores das barras no gráfico
# ax = sns.barplot(x='Sigla UF', y='Média', data=media_tipoEscola_porUF, palette = cores2)
# for p in ax.patches:
#     ax.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()),\
#                  ha = 'center', va = 'center', xytext = (5, 15), textcoords = 'offset points', rotation=45,\
#                     fontsize =9, color='grey')
# # Ajustar a estética do gráfico
# sns.set(style='whitegrid')
# plt.title('Nota Média por UF', y=1.03)
# plt.xlabel('UF')
# plt.ylabel('Nota Média')
# plt.ylim(400, 600)
# plt.xticks(color='grey')
# plt.yticks(color='grey')


# #Grid
# ax.yaxis.grid(True, alpha=0.1)
# ax.set_axisbelow(True)
# # Borda top e right invisiveis
# ax.spines['top'].set_visible(False)
# ax.spines['left'].set_visible(False)
# ax.spines['right'].set_visible(False)
# # Mostrar o gráfico
# plt.show()