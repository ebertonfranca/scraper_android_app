import pandas as pd
from collections import Counter
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json
import nltk
from datetime import datetime

nltk.download('punkt')

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Usar a chave API carregada do arquivo de ambiente
llm = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo')

def load_comments(json_file):
    """Load comments from a JSON file with multiple lines of JSON objects."""
    comments = []
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            for line in f:
                comment = json.loads(line.strip())
                if 'content' in comment and 'date' in comment:
                    comments.append({
                        'content': comment['content'],
                        'date': comment['date']
                    })
    except FileNotFoundError:
        print(f"Erro: O arquivo {json_file} não foi encontrado.")
    except json.JSONDecodeError as e:
        print(f"Erro ao ler o arquivo {json_file}: {e}")
    except Exception as e:
        print(f"Erro ao ler o arquivo {json_file}: {e}")
    return comments

def create_prompt_template(case_of_use):
    templates = {
        "analise_sentimento": (
            "Analisar o sentimento dos seguintes comentários (positivo, negativo, neutro):\n{comments}. "
            "O resultado deve ser um JSON estruturado com os seguintes campos: "
            "'Tabela de Sentimentos' (um dicionário com a contagem de cada sentimento), "
            "'Comentários por Tópicos' (um dicionário com listas de comentários categorizados por sentimento e obrigatoriamente a data do sentimento, cada comentário separado por chaves, contendo data, comentário e resultado), "
            "e 'Análise para o Conselho Executivo' (um texto de no máximo 10 linhas)."
        )
    }
    return templates.get(case_of_use, "")

def save_to_json(data, base_filename):
    """Save data to a JSON file with a unique name."""
    try:
        filename = base_filename
        counter = 1
        while os.path.exists(filename):
            filename = f"{base_filename.rstrip('.json')}{counter}.json"
            counter += 1
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Resultados salvos em {filename}")
    except Exception as e:
        print(f"Erro ao salvar os resultados em {filename}: {e}")

def analyze_sentiment(comments):
    """Analyze sentiment of comments."""
    try:
        prompt_template = create_prompt_template('analise_sentimento')
        prompt = PromptTemplate.from_template(prompt_template)
        llm_chain = prompt | llm
        formatted_comments = "\n".join([f"{comment['date']} - {comment['content']}" for comment in comments])
        response = llm_chain.invoke(formatted_comments)
        
        # Print the response for debugging
        print("Response from model:")
        print(response.content)
        
        # Parse the JSON response
        result = json.loads(response.content)
        
        # Print the result for debugging
        print("Result to be saved:")
        print(json.dumps(result, ensure_ascii=False, indent=4))
        
        # Get current date for filename
        current_date = datetime.now().strftime("%d_%m_%Y")
        base_filename = f"{current_date}_android_analysis_sentiment.json"
        save_to_json(result, base_filename)
    except Exception as e:
        print(f"Erro ao analisar sentimentos: {e}")

def print_header(header):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(header)
    print("=" * 80)

# Exemplo de uso
if __name__ == "__main__":
    json_file = "/mnt/data/14_06_2024_google_play_review.json"  # Substitua pelo nome do seu arquivo de comentários
    comments = load_comments(json_file)
    if comments:
        analyze_sentiment(comments)

