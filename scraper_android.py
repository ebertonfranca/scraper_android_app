import pandas as pd
import numpy as np
from google_play_scraper import reviews, Sort
import matplotlib.pyplot as plt  # Certifique-se de que matplotlib está instalado

# Configurações do aplicativo
google_play_app_id = 'br.com.vivo.vivoeasy'  # ID correto do aplicativo no Google Play
lang = 'pt'  # Idioma português
country = 'br'  # País Brasil

# Função para extrair e salvar análises do Google Play
def scrape_google_play_reviews(app_id, lang, country, count=15):
    result, _ = reviews(
        app_id,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=count
    )

    if not result:
        print("Nenhuma análise encontrada no Google Play.")
        return None
    else:
        reviews_df = pd.DataFrame(np.array(result), columns=['review'])
        reviews_df_expanded = reviews_df.join(pd.DataFrame(reviews_df.pop('review').tolist()))
        
        # Ajustar o DataFrame para incluir somente as colunas relevantes
        reviews_df_expanded = reviews_df_expanded[['content', 'score']]
        
        reviews_df_expanded.to_json('google_play_reviews.json', orient='records', lines=True, force_ascii=False)
        print("Análises do Google Play salvas em 'google_play_reviews.json'")
        return reviews_df_expanded

# Extrai e salva análises do Google Play
google_play_reviews_df = scrape_google_play_reviews(google_play_app_id, lang, country)

# Exibe as primeiras linhas dos DataFrames resultantes
if google_play_reviews_df is not None:
    print("Google Play Reviews:")
    print(google_play_reviews_df.head())