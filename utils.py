import pandas as pd
from collections import Counter
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json
import nltk

nltk.download('punkt')

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Verifique se a chave da API foi carregada corretamente
if not openai_api_key:
    raise ValueError("A chave da API do OpenAI não foi encontrada. Verifique o arquivo .env.")

# Usar a chave API carregada do arquivo de ambiente
llm = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo')

def load_comments(json_file):
    """Load comments from a JSON file with multiple lines of JSON objects."""
    comments = []
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            for line in f:
                comment = json.loads(line.strip())
                if 'content' in comment:
                    comments.append(comment['content'])
    except FileNotFoundError:
        print(f"Erro: O arquivo {json_file} não foi encontrado.")
    except json.JSONDecodeError as e:
        print(f"Erro ao ler o arquivo {json_file}: {e}")
    except Exception as e:
        print(f"Erro ao ler o arquivo {json_file}: {e}")
    return comments

def create_prompt_template(case_of_use):
    templates = {
        "analise_sentimento": "Analisar o sentimento dos seguintes comentários (positivo, negativo, neutro):\n{comments}. O resultado deve conter o comentário e o resultado, além de uma tabela com os sentimentos e a contagem total de cada um. Crie também um texto de no máximo 10 linhas que possa dar uma visão ao conselho executivo do cenário geral considerando a análise dos comentários."
    }
    return templates.get(case_of_use, "")

def save_to_json(data, filename):
    """Save data to a JSON file."""
    try:
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
        response = llm_chain.invoke("\n".join(comments))

        # Print the response for debugging
        print("Response from model:")
        print(response.content)

        # Process response to extract sentiment analysis and summary
        response_lines = response.content.split('\n')

        # Extract sentiment analysis
        comment_analysis = {"Negativo": [], "Positivo": [], "Neutro": []}
        summary = []
        sentiment_counts = Counter()

        for line in response_lines:
            if " - " in line:
                parts = line.split(" - ")
                if len(parts) == 2:
                    comment = parts[0].strip().strip('"')
                    sentiment = parts[1].strip()
                    if sentiment in comment_analysis:
                        comment_analysis[sentiment].append(comment)
                        sentiment_counts[sentiment] += 1
            elif line.startswith("Tabela de Sentimentos:"):
                continue  # Skip the header
            elif line.startswith("Análise para o conselho executivo:"):
                summary.append(line)
            elif summary:
                summary.append(line)

        # Remove unnecessary prefix from the summary
        summary = [line.replace("Análise para o conselho executivo:", "").strip() for line in summary]

        # Print the analysis
        print_header("Análise de Sentimento")
        print("\nAnálise dos sentimentos:")
        for sentiment, count in sentiment_counts.items():
            print(f"- {sentiment}: {count}")

        for sentiment in ["Negativo", "Positivo", "Neutro"]:
            print(f"\n{sentiment}s:")
            if comment_analysis[sentiment]:
                for comment in comment_analysis[sentiment]:
                    print(f"- {comment}")
            else:
                print(f"Sem análises {sentiment.lower()}s.")
        print("\n")

        for line in summary:
            print(line)

        # Save to JSON
        result = {
            "Tabela de Sentimentos": dict(sentiment_counts),
            "Comentários por Tópicos": comment_analysis,
            "Análise para o Conselho Executivo": " ".join(summary).strip()
        }

        # Print the executive summary to ensure it's captured
        print("\nAnálise para o Conselho Executivo:")
        print(result["Análise para o Conselho Executivo"])

        save_to_json(result, "android_sentiment_analysis.json")
    except Exception as e:
        print(f"Erro ao analisar sentimentos: {e}")

def print_header(header):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(header)
    print("=" * 80)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Uso: python app.py <caso_de_uso|todos> <arquivo_json>")
        sys.exit(1)
    case_of_use = sys.argv[1]
    json_file = sys.argv[2]
    comments = load_comments(json_file)
    if case_of_use == "analise_sentimento":
        print_header("Análise de Sentimento")
        analyze_sentiment(comments)
    else:
        print("Caso de uso inválido")