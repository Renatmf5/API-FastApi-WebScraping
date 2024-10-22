# FastAPI API Documentation

- Este repositório contém a implementação de uma API desenvolvida em FastAPI para manipular dados relacionados a produção, importação, exportação e comercialização de produtos. A aplicação também faz uso de machine learning para previsões de dados e armazena arquivos em um data lake no AWS S3.

# Funcionalidades

- **Autenticação via JWT**: A API utiliza autenticação baseada em JWT para proteger os endpoints.
- **Operações com AWS S3**: Faz upload e download de arquivos para o S3 e manipula arquivos em formato Parquet.
- **Previsões com Machine Learning**: Modelos de previsão para diferentes produtos baseados em séries temporais.
- **Web Scraping**: Extrai dados de URLs específicas e armazena no data lake S3.

# Endpoints

- **Autenticação**: 
  - **POST /usuarios/login**: Autentica um usuário e retorna um token JWT.
    - **Parâmetros**:
      -- **username**: string - Nome de usuário
      -- **password**: string - Senha do usuário
    - **Resposta**: 
     - **200 OK**: Token JWT válido
     - **401 Unauthorized**: Credenciais inválidas

  - **POST /usuarios/signup**: Cria um novo usuário.
    - **Parâmetros**:
        -- **username**: string - Nome de usuário
        -- **password**: string - Senha do usuário
        - **admin**: boolean (opcional) - Indica se o usuário terá privilégios de administrador
      - **Resposta**: 
      - **201 Created**: Usuário criado com sucesso
      - **406 Not Acceptable**: Nome de usuário já está em uso

- **Endpoints de Manipulação de Dados**:
  - **GET /producao/download-arquivo**: Baixa os dados de produção e envia para o Data Lake (S3).
  - **GET /comercializacao/download-arquivo**: Baixa os dados de comercialização e envia para o S3.
  - **GET /fetch-data/tables**: Lista os arquivos no S3.
  - **GET /fetch-data**: Busca dados filtrados de arquivos específicos no S3.

- **Machine Learning**:
  - **GET /ml-models/train**: Treina modelos de previsão usando dados do S3.
  - **GET /ml-models/predict**: Gera previsões futuras com base em dados existentes.

# Instalação e Execução

- **Pré-requisitos**
  - **Python 3.10.2+**
  - **AWS CLI** configurado com as credenciais apropriadas

**Instalação**
1. Clone o repositório:
```bash
-  https://github.com/Renatmf5/API-FastApi-WebScraping.gitt
-  cd API-FastApi-WebScraping
```
2. Crie e ative um ambiente virtual:
```bash
- python -m venv venv
- source venv/bin/activate
```
3. Instale as dependências:
```bash
- pip install -r requirements.txt
```

4. Configure as variáveis de ambiente: Crie um arquivo .env com as variáveis necessárias:
```env
- JWT_SECRET= qualquer chave para usar no algoritmo HS256
- DATABASE_URL=sqlite:///./authDB.db
- BUCKET_NAME=nome do bucket de Data Lake
- ENV=development para rodar local
```

# Executando localmente

1. Inicie a aplicação FastApi:
```bash
- python main.py
```