#!/bin/bash
DIR="/home/ec2-user/fastapi-app"

echo "ApplicationStart: Iniciando a aplicação"

# Conceder permissões
sudo chmod -R 777 ${DIR}

# Navegar para o diretório da aplicação
cd ${DIR}

# Executar o comando uvicorn para iniciar a aplicação FastAPI em segundo plano e redirecionar a saída
nohup uvicorn main:app --host 0.0.0.0 --port 80 > /dev/null 2>&1 &