import json
import glob
import pandas as pd
import streamlit as st
import altair as alt

def carregar_dados(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            data = corrigir_chaves(data)
            return data
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo JSON {file_path}: {e}")
        return None

def corrigir_chaves(data):
    # Normalizar chaves para lidar com variações
    if "Comentários por Tópicos" in data:
        data["Comentários por Tópicos"] = {k.lower(): v for k, v in data["Comentários por Tópicos"].items()}
        for key in data["Comentários por Tópicos"]:
            for item in data["Comentários por Tópicos"][key]:
                if "comentário" in item:
                    item["comentario"] = item.pop("comentário")
    return data

# Adicionar imagem na barra lateral
st.sidebar.image("https://play-lh.googleusercontent.com/NMdtfQlSntvyVOYwAD0Nrhy4Ii7xzoG0azA-_q6dviw3o0w0RLuFid3VI9MrhAvsHsI=w240-h480-rw", use_column_width=True)

# Listar todos os arquivos JSON disponíveis que terminam com "analysis_sentiment.json"
arquivos_json = glob.glob("*analysis_sentiment.json")

# Criar seleção de data na barra lateral sem seleção padrão
arquivos_selecionados = st.sidebar.multiselect('Selecione a data de análise', arquivos_json, default=[])

# Verificar se algum arquivo foi selecionado
if not arquivos_selecionados:
    st.warning("Nenhum arquivo selecionado. Por favor, selecione ao menos um arquivo JSON.")
    st.stop()

# Carregar dados dos arquivos selecionados
dados_completos = []
for arquivo in arquivos_selecionados:
    dados = carregar_dados(arquivo)
    if dados:
        dados_completos.append(dados)

# Verificar se há dados carregados
if not dados_completos:
    st.error("Nenhum dado carregado. Por favor, selecione ao menos um arquivo JSON válido.")
    st.stop()

# Unir os dados dos arquivos selecionados
comentarios_df = pd.DataFrame()
analises_conselho = []
for data in dados_completos:
    comentarios_por_topicos = data["Comentários por Tópicos"]
    analises_conselho.append(data["Análise para o Conselho Executivo"])
    for sentimento, comentarios in comentarios_por_topicos.items():
        df = pd.DataFrame(comentarios)
        df['sentimento'] = sentimento
        comentarios_df = pd.concat([comentarios_df, df])

# Converter coluna de data para datetime
try:
    comentarios_df['data'] = pd.to_datetime(comentarios_df['data'], format='%d-%m-%Y')
except Exception as e:
    st.error(f"Erro ao converter datas: {e}")
    st.stop()

# Determinar a data mais recente nos dados carregados
data_titulo = comentarios_df['data'].max().strftime('%d-%m-%Y')

# Título do Dashboard
st.title(f"Análise de sentimentos e reviews - Google Play")

# Gráfico de barras com tópicos e quantidade por tópico
st.header('Quantidade de Comentários por Tópico')
topicos_count = comentarios_df['sentimento'].value_counts().reindex(['positivo', 'neutro', 'negativo'], fill_value=0).reset_index()
topicos_count.columns = ['sentimento', 'count']

# Definir cores para os sentimentos
color_scale = alt.Scale(domain=['positivo', 'neutro', 'negativo'], range=['green', 'gray', 'red'])

# Criar gráfico de barras
bar_chart = alt.Chart(topicos_count).mark_bar().encode(
    x=alt.X('sentimento:N', title='Sentimento'),
    y=alt.Y('count:Q', title='Quantidade'),
    color=alt.Color('sentimento:N', scale=color_scale, legend=None)
).properties(
    width=600, height=400
)

# Adicionar rótulos às barras
text = bar_chart.mark_text(
    align='center',
    baseline='middle',
    dy=-10,  # Deslocamento vertical
    color='white'
).encode(
    text='count:Q'
)

# Combinar o gráfico de barras e os rótulos
final_chart = bar_chart + text
st.altair_chart(final_chart)

# Filtro para selecionar por tópico
st.sidebar.header('Filtrar por Tópico')
topicos = st.sidebar.radio('Escolha o tópico', ['Todos', 'positivo', 'neutro', 'negativo'])
if topicos != 'Todos':
    comentarios_df = comentarios_df[comentarios_df['sentimento'] == topicos]

# Lista de comentários ordenada por data
st.header('Comentários')
for index, row in comentarios_df.iterrows():
    if row['sentimento'] == 'positivo':
        sentimento_color = 'green'
    elif row['sentimento'] == 'neutro':
        sentimento_color = 'gray'
    else:
        sentimento_color = 'red'
    
    comentario = row.get('comentario', 'Comentário não disponível')
    st.markdown(f"<p style='color:white;'><b>{row['data'].strftime('%d-%m-%Y')}:</b> {comentario} <span style='color:{sentimento_color};'>({row['sentimento']})</span></p>", unsafe_allow_html=True)

# Campo de texto com a "Análise para o Conselho Executivo"
st.header('Análise do sentimento dos usuários')
st.text_area('-', ' '.join(analises_conselho), height=200)





