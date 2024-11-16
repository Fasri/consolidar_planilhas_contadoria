import pandas as pd

# Carregar os arquivos
liquidacao = pd.read_csv('liquidacao.csv')
custas = pd.read_csv('custas.csv')
tempo_real = pd.read_excel('final_tempo_real.xlsx')

# Selecionar colunas específicas de liquidacao
liquidacao = liquidacao[['Tipo', 'Núcleo', 'Posição Geral', 'Posição Prioridade',
       'Número do processo', 'Vara', 'Data Remessa Contadoria',
       'Data Remessa Antiga', 'Prioridade', 'Crítico', 'Natureza',
       'Calculista', 'Data da atribuição', 'Cumprimento', 'Data da conclusão', 
       'Valor Total Devido - Custas', 'Observações', 'Tempo na contadoria', 
       'Tempo para atribuir', 'Tempo com o Contador', 'Meta']]

# Mesclar liquidacao e custas
consolidacao = pd.concat([liquidacao, custas], axis=0, ignore_index=True)

# Renomear colunas de tempo_real para corresponder às de consolidacao
tempo_real.rename(columns={
    'nucleo': 'Núcleo',
    'processo': 'Número do processo',
    'vara': 'Vara',
    'data': 'Data Remessa Contadoria',
    'dias': 'Tempo na contadoria',
    'prioridades': 'Prioridade'
}, inplace=True)

# Filtrar tempo_real para incluir processos com o mesmo número, mas data de remessa diferente
novos_processos = tempo_real[~tempo_real.set_index(['Número do processo', 'Data Remessa Contadoria']).index
    .isin(consolidacao.set_index(['Número do processo', 'Data Remessa Contadoria']).index)]

# Adicionar a coluna 'Cumprimento' com valor 'Pendente' para novos processos
novos_processos['Cumprimento'] = 'Pendente'

# Concatenar novos processos ao DataFrame consolidacao
consolidacao = pd.concat([consolidacao, novos_processos], axis=0, ignore_index=True)

# Exibir o número de linhas do DataFrame consolidado atualizado
print(f"Número de linhas em consolidacao após adição: {len(consolidacao)}")

# Contar a quantidade de processos onde 'Cumprimento' é 'Pendente'
pendentes_count = len(consolidacao[consolidacao['Cumprimento'] == 'Pendente'])
print(f"Quantidade de processos pendentes: {pendentes_count}")

# Salvar o DataFrame consolidado atualizado
consolidacao.to_csv('consolidacao.csv', index=False, encoding='utf-8')
consolidacao.to_excel('consolidacao.xlsx',sheet_name='consolidacao', index=False)
def load_tempo_real():
    import os.path

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import pandas as pd

    # Autenticação
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = '/home/felipe/acompamhamento_contadoria/acompamhamento_contadoria/pipeline/credentials.json'  # Caminho para o seu arquivo credentials.json

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "/home/felipe/consolidacao/credentials.json", SCOPES
        )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # ID da planilha do Google Sheets
    SPREADSHEET_ID = '1awhOgdpa_Kkwsj3NxFnlCVPGJPdM3bR6kasS7alyOVc'


    # Leitura do arquivo XLS local, incluindo todas as abas
    file_path = 'consolidacao.xlsx'

    sheets = pd.read_excel(file_path, sheet_name=None)  # Lê todas as abas


    for sheet_name, df in sheets.items():
        # Convertendo DataFrame para lista de listas
        values = [df.columns.values.tolist()] + df.values.tolist()
    
        # Preparação dos dados
        body = {
            'values': values
        }         
        
        # Limpeza do conteúdo existente e atualização com novos dados
        range_name = f'{sheet_name}!A1:w600000'  # Define o range para cada aba
        service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=range_name,
            valueInputOption='RAW', body=body).execute()

        print(f'{result.get("updatedCells")} células atualizadas na aba {sheet_name}.')

load_tempo_real()