import sys
from utils import (load_comments, analyze_sentiment, print_header)

import sys
from utils import (load_comments, analyze_sentiment, print_header)

def main():
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

if __name__ == "__main__":
    main()