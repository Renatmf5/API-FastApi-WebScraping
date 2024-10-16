#!/bin/bash
DIR="/home/ec2-user/fastapi-app"

echo "ApplicationStart: Iniciando a aplicação"

# Conceder permissões
sudo chmod -R 777 ${DIR}

# Navegar para o diretório da aplicação
cd ${DIR}

# Definir variável de ambiente
export ENV=production

# Executar o comando uvicorn para iniciar a aplicação FastAPI em segundo plano e redirecionar a saída para um arquivo de log
nohup uvicorn main:app --host 0.0.0.0 --port 80 > app.log 2>&1 &