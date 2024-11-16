import pandas as pd

liquidacao = pd.read_csv('liquidacao.csv')
custas = pd.read_csv('custas.csv')
tempo_real=pd.read_excel('final_tempo_real.xlsx')
tempo_real.to_csv('tempo_real.csv', index=False, encoding='utf-8')

print(liquidacao.columns)

liquidacao = liquidacao[['Tipo', 'Núcleo', 'Posição_Geral', 'Posição_Prioridade',
       'Número_do_processo', 'Vara', 'Data Remessa \nContadoria',
       'Data Remessa \nAntiga', 'Prioridade', 'Crítico', 'Natureza',
       'Calculista', 'Data_da_atribuição',
       'Cumprimento', 'Data_da_conclusão', 'Valor_Total_Devido_Custas',
       'Observações', 'Tempo na contadoria', 'Tempo_para_atribuir',
       'Tempo_com_o_Contador', 'Meta',]]
print(liquidacao.head())
print(liquidacao.columns)

#mesclar liquidacao e custas

consolidacao = pd.concat([liquidacao, custas], axis=0, ignore_index=True)


print(consolidacao.columns)

#quantas linhas tem a consolidacao

print(len(consolidacao))

consolidacao.to_csv('consolidacao.csv', index=False, encoding='utf-8')

tempo_real=pd.read_excel('tempo_real.xlsx')
tempo_real.to_csv('tempo_real.csv', index=False, encoding='utf-8')
#adicionar tempo real na consolidacao


