# Limpeza de Dados de E-commerce
Descrição
Este projeto visa a limpeza e padronização de um conjunto de dados brutos extraídos de um e-commerce. O objetivo é preparar o dataset para futuras análises e modelos de machine learning. As operações incluem tratamento de valores nulos, padronização de formatos e limpeza de informações irrelevantes.

#Estrutura dos Dados Antes da Limpeza
O conjunto de dados original possui diversas colunas com informações sobre os produtos do e-commerce. Antes da limpeza, a estrutura dos dados apresenta algumas inconsistências e valores ausentes, que foram tratados no processo de limpeza.

- Colunas Originais
goods-title-link--jump: Nome do produto (pode conter valores duplicados ou incompletos).
price: Preço do produto (inclui o símbolo $ e pode ter valores ausentes ou inválidos).
goods-title-link--jump href: URL do produto (alguns links podem estar quebrados ou inválidos).
selling proposition: Proposta de venda, como "500+ sold recently" (muitos valores nulos e inconsistências no formato dos dados).
discount: Desconto no produto, no formato de string com % (necessita de conversão para valores numéricos).
outros: Outras colunas que podem conter dados irrelevantes ou inconsistentes para a análise.
Principais Problemas Identificados:
Valores Nulos: Muitas colunas contêm valores nulos que precisaram ser tratados.
Formato Inconsistente: Várias colunas têm valores no formato de string com caracteres que precisam ser removidos ou convertidos para tipos numéricos (ex.: % em discount, $ em price).
Links Inválidos: Algumas URLs na coluna goods-title-link--jump href estão quebradas ou fora do padrão esperado.
Propostas de Venda: A coluna selling proposition apresenta muitos valores nulos e um formato que mistura texto e números, dificultando o uso direto em análises.

# Estrutura dos Dados Após limpeza
product_name: Nome do produto (texto)
price_USD: Preço do produto em dólares (float)
discount: Percentual de desconto aplicado (float, de 0 a 1)
sold_recently: Quantidade de unidades vendidas recentemente (inteiro)
product_link: URL do produto (texto)
is_valid_link: Verifica se o link do produto é válido (boolean)

# Passos de Limpeza
Tratamento de valores nulos:

Substituição de valores nulos nas colunas selling_proposition e discount por valores padrão, como 'unknown' e 0, respectivamente.

Remoção de caracteres:

Limpeza de símbolos como % em colunas de desconto, convertendo esses valores em números decimais adequados.

Padronização de Links:

Verificação da validade das URLs dos produtos para garantir que seguem um padrão específico.



## Como Usar

1. Abra o arquivo `limpeza_dados_ecommerce.ipynb` em um ambiente Jupyter.
2. Execute as células sequencialmente para realizar a limpeza de dados.
3. Certifique-se de que o ambiente Python contém a biblioteca Pandas
