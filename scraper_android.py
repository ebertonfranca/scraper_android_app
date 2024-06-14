import pandas as pd
import numpy as np
from google_play_scraper import reviews, Sort
import datetime
import os

# Configurações do aplicativo
google_play_app_id = 'br.com.vivo.vivoeasy'  # ID correto do aplicativo no Google Play
lang = 'pt'  # Idioma português
country = 'br'  # País Brasil

# Função para extrair e salvar análises do Google Play
def scrape_google_play_reviews(app_id, lang, country, count=50):
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
        
        # Ajustar o DataFrame para incluir as colunas relevantes
        reviews_df_expanded = reviews_df_expanded[['content', 'score', 'at']]
        reviews_df_expanded['at'] = reviews_df_expanded['at'].dt.strftime('%d-%m-%Y')
        reviews_df_expanded.rename(columns={'at': 'date'}, inplace=True)

        # Adicionar a data no nome do arquivo
        date_str = datetime.datetime.now().strftime('%d_%m_%Y')
        base_filename = f"{date_str}_google_play_review"
        counter = 1
        filename = f"{base_filename}.json"

        while os.path.exists(filename):
            filename = f"{base_filename}_{counter}.json"
            counter += 1
        
        reviews_df_expanded.to_json(filename, orient='records', lines=True, force_ascii=False)
        print(f"Análises do Google Play salvas em '{filename}'")
        return reviews_df_expanded

# Extrai e salva análises do Google Play
google_play_reviews_df = scrape_google_play_reviews(google_play_app_id, lang, country)

# Exibe as primeiras linhas dos DataFrames resultantes
if google_play_reviews_df is not None:
    print("Google Play Reviews:")
    print(google_play_reviews_df.head())