#!/usr/bin/env python3

import pandas as pd  # importa a biblioteca pandas
from ortools.linear_solver import pywraplp  # importa o pywraplp da biblioteca ortools
from tabulate import tabulate  # Importa o tabulate

# Carregando os dados
dados_mkt = pd.read_csv('Desafio_de_negócio_com_programacao_linear.csv')  # importa o arquivo csv

# Resolução
solver = pywraplp.Solver.CreateSolver('SCIP')  # Cria um solver para programação inteira mista

lim_min_facebook = 5000  # Mínimo de investimento Facebook Ads
lim_max_facebook = 15000  # Máximo de investimento Facebook Ads

lim_min_google = 10000  # Mínimo de investimento Google Ads
lim_max_google = 25000  # Máximo de investimento Google Ads

lim_min_email = 2000  # Mínimo de investimento Email
lim_max_email = 10000  # Máximo de investimento Email

custo_conv_fb = 20  # Custo de conversão Facebook Ads
custo_conv_google = 15  # Custo de conversão Google Ads
custo_conv_email = 10  # Custo de conversão Email

# ROI por dólar investido
roi_facebook = 3
roi_google = 2.5
roi_email = 1.8

# Define variáveis de conversão
facebook_investimento = solver.NumVar(lim_min_facebook, lim_max_facebook, 'Facebook Ads')
google_investimento = solver.NumVar(lim_min_google, lim_max_google, 'Google Ads')
email_investimento = solver.NumVar(lim_min_email, lim_max_email, 'Email Marketing')

orcamento_total = 50000  # Define nosso limite de gasto

# Define nosso orçamento total como restrição
solver.Add(facebook_investimento + google_investimento + email_investimento <= orcamento_total)

# Calculo do ROI total
total_roi = (
    (facebook_investimento / custo_conv_fb) * roi_facebook +
    (google_investimento / custo_conv_google) * roi_google +
    (email_investimento / custo_conv_email) * roi_email
)

# Define a maximização do ROI total
solver.Maximize(total_roi)

# Resolve o problema com o solver
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    # Calculo do ROI total
    roi_total = (
        (facebook_investimento.solution_value() / custo_conv_fb) * roi_facebook +
        (google_investimento.solution_value() / custo_conv_google) * roi_google +
        (email_investimento.solution_value() / custo_conv_email) * roi_email
    )

    # Estrutura os dados para exibição
    data = [
        ['Facebook Ads', '${:.2f}'.format(facebook_investimento.solution_value())],
        ['Google Ads', '${:.2f}'.format(google_investimento.solution_value())],
        ['Email Marketing', '${:.2f}'.format(email_investimento.solution_value())],
        ['ROI Total', '${:.2f}'.format(roi_total)]
    ]

    print(tabulate(data, tablefmt='rounded_grid'))

else:
    erro = [
        ['O problema não apresenta solução viável']  # Caso contrário, exiba uma mensagem de erro
    ]
    print(tabulate(erro, tablefmt='rounded_grid'))
