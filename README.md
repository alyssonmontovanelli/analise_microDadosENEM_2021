<h1 align="center"> Análise dos Micro Dados do ENEM/2021</h1>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

<h2>Descrição do Projeto</h2>
<p>Esse projeto foi desenvolvido com o intuito de realizar uma análise profunda nos dados brutos do ENEM/2021. Para então traçar um panorama do ensino no país, bem como o perfil dos inscritos.</p>
<p>O relatório com toda informação gerada, auxiliada por diversos gráficos está publicada no meu perfil do medium, através do link abaixo:</p>

[![Confira o artigo no Medium!](https://img.shields.io/badge/Medium-Profile-black?logo=medium)](https://medium.com/@alysson.montovanelli/an%C3%A1lise-dos-micro-dados-do-enem-2021-um-panorama-sobre-o-ensino-brasileiro-e-perfil-dos-inscritos-c6e317447c07)

<p>Os micro dados utilizados neste projetos foram baixados no portal de dados abertos do governo federal, o arquivo CSV não está anexado a este repositório, por ser pesado demais, tendo 1.40 GB e shape de (3.383.000 x 77)</p>

<h2>Divisão do Projeto</h2>
<ul>
 <li>Main.py</li>
 <li>Arquivo 'filtroDados'</li>
 ➜ <b>escolaNota.py</b> <br>
 Arquivo destinado ao tratamento e modelagem dos dados relacionados ao impacto dos tipos de escolas no desempenho <br>
 ➜ <b>inscritosGeral.py</b> <br>
 Arquivo destinado ao tratamento e modelagem dos dados relacionados gerais de candidatos <br>
 ➜ <b>redacaoNota.py</b> <br>
 Modelagem do panorama geral e status das redações do ENEM, bem como do desempenho dos estudantes<br>
 ➜ <b>socio_economico.py</b> <br>
 Modelagem dos dados referente ao fator socioeconomico dos candidatos, e o impacto deste no desempenho final
 ➜ <b>utils.py</b>
 arquivo destinados aos import's, arrays com os filtros das tabelas e dicionários para conversão dos dados.
 <li>Arquivo 'graphics'</li>
 ➜ Pasta destinada aos gráficos gerados com matplotlib e seaborn
</ul>

<h3>Análise exploratória</h3>

<p>Formato dos dados CSV, shape(3.389.832 x 77):</P>
<img src="graphics\readme\arquivo_csv.png" alt="Descrição da imagem" width="600" height="200">
<br><br>
<p>Criação de arrays com os nomes das colunas necessárias a cada análise:</P>
<img src="graphics\readme\utils.png" alt="Descrição da imagem" width="600" height="200">
<br><br>
<p>Já nos arquivos de cada análise, preparei os dados com base na sequência: criação do dataframe utilizando o array correspondente de 'utils.py' / verificação de valores ausentes ou nulos / criação de uma coluna com valores 'Presente' ou 'Eliminado', com base nos valores ausentes das notas de cada disciplina / criação de coluna para a nota média geral de cada inscrito. No caso abaixo, como as quantidades de valores ausentes das colunas "Q00.." são inexpressivas, atribuí valores recorrentes. </P>
<img src="graphics\readme\utils2.png" alt="Descrição da imagem" width="600" height="200">
<br><br>
<p>Após isso, iniciei as consultas para posterior plotagem e confecção de relatório final, que está postado no Medium:</P>
<img src="graphics\readme\consultas.png" alt="Descrição da imagem" width="600" height="200">