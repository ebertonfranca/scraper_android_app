Scraper Android App
Este projeto fornece scripts para raspar análises de aplicativos da Google Play Store, analisar os sentimentos dessas análises e identificar questões comuns.

Estrutura do Projeto

1. scraper_android.py: Script que faz a raspagem de dados no Google Play Store
2. app.py: Script principal para rodar análises de sentimento.
3. utils.py: Contém funções utilitárias para carregar comentários, analisar sentimentos e imprimir cabeçalhos.
4. test.py: Contém testes para as funções principais.

Dependências

4. As dependências para este projeto incluem bibliotecas de terceiros como pandas, nltk, langchain, dotenv, entre outras.

Instalação

5. Clone o repositório:
Por exemplo, para código Ruby do realce de sintaxe:

```ruby
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

6. Crie um ambiente virtual (opcional, mas recomendado):

```ruby
python -m venv venv
source venv/bin/activate  # Para Linux e macOS
.\venv\Scripts\activate  # Para Windows
```

7. Instale as dependências:

```
pip install -r pandas nltk langchain openai python-dotenv
```

8. Executar o Script de raspagem

Para executar o script principal app.py, use o seguinte comando:

```ruby
python scraper_android.py
```

8. Executar o Script de análise de sentimentos

```ruby
python app.py analise_sentimento google_play_reviews.json
```

Neste função você pode alterar a quantidade de reviews raspados da Google Play no count=5

```ruby
def scrape_google_play_reviews(app_id, lang, country, count=5):
```

9. Executar testes

Explicação das Funções de Teste

test_load_comments():

Cria dados JSON simulados.

Escreve esses dados em um arquivo temporário mock_google_play_reviews.json.
Carrega os comentários usando a função load_comments.
Verifica se os comentários carregados correspondem aos dados simulados.

test_analyze_sentiment():

Utiliza uma lista de comentários simulados.

Chama a função analyze_sentiment para analisar os sentimentos dos comentários.

test_print_header():

Testa a função print_header imprimindo um cabeçalho de teste.

- Execute o script test.py para rodar os testes:

```ruby
python test.py
```

10. Output:

================================================================================
Análise de Sentimento
================================================================================

Análise dos sentimentos:
- Positivo: 2
- Negativo: 2
- Neutro: 1

Negativos:
- 3. Aplicativo patético Não funciona de jeito nenhum fica carregando infinito diversas vezes que você tentar entrar
- 4. Não consigo adicionar um novo cartão, já entrei em contato mas eles não conseguem resolver o problema.

Positivos:
- 1. Ótimo aplicativo, funciona bem.
- 2. A independência e os benefícios valem cada centavo investido.

Neutros:
- 5. Opção boa para uso na área externa.

- 6. Análise para o Conselho Executivo
Considerando a análise dos comentários dos usuários, podemos observar que o aplicativo possui uma divisão equilibrada entre comentários positivos e negativos. Enquanto alguns usuários elogiaram o funcionamento e os benefícios do aplicativo, outros relataram problemas de carregamento e dificuldades no atendimento ao cliente. É importante avaliar as áreas em que o aplicativo está se destacando positivamente e buscar soluções para os problemas apontados pelos usuários. Investir em melhorias na usabilidade e no suporte ao cliente pode contribuir para uma experiência mais satisfatória e fidelização dos usuários.
Resultados salvos em android_sentiment_analysis.json
