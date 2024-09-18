import json
import boto3
import psycopg2
import pandas as pd
import os
from fastapi import HTTPException
from core.config import settings
from io import BytesIO
from core.services.parameterServiceAws import get_ssm_parameter

def map_dtype_to_redshift(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return 'BIGINT'
    elif pd.api.types.is_float_dtype(dtype):
        return 'DOUBLE PRECISION'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'TIMESTAMP'
    else:
        return 'VARCHAR'


def process_s3_to_redshift(file_name: str):
    try:
         # Configurações do S3 e Redshift a partir do SSM Parameter Store
        redshift_cluster = get_ssm_parameter('/techchallenge_fase1/redshift/cluster-endpoint')
        redshift_database = get_ssm_parameter('/techchallenge_fase1/redshift/database')
        redshift_user = get_ssm_parameter('/techchallenge_fase1/redshift/user')
        redshift_password = get_ssm_parameter('/techchallenge_fase1/redshift/password')
        redshift_port = int(get_ssm_parameter('/techchallenge_fase1/redshift/port'))
        redshift_role = get_ssm_parameter('/techchallenge_fase1/redshift/role')
        
        # Conectar ao Redshift
        conn = psycopg2.connect(
            dbname=redshift_database,
            user=redshift_user,
            password=redshift_password,
            port=redshift_port,
            host=redshift_cluster
        )
        cursor = conn.cursor()
        
        s3_client = boto3.client('s3')
        
        # Baixar o arquivo do S3
        response = s3_client.get_object(Bucket=settings.BUCKET_NAME, Key=file_name)
        file_content = response['Body'].read()
        df = pd.read_parquet(BytesIO(file_content))
        
         # Criar a tabela no Redshift se não existir
        table_name = file_name.split('/')[-1].split('.')[0]  # Nome da tabela baseado no nome do arquivo
        columns = ', '.join([f'{col} {map_dtype_to_redshift(dtype)}' for col, dtype in df.dtypes.items()])
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns}
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        
        # Limpar a tabela se ela já existir
        clear_table_query = f"DELETE FROM {table_name};"
        cursor.execute(clear_table_query)
        conn.commit()
        
       # Usar o comando COPY para carregar os dados do Parquet para o Redshift
        copy_query = f"""
        COPY {table_name}
        FROM 's3://{settings.BUCKET_NAME}/{file_name}'
        IAM_ROLE '{redshift_role}'
        FORMAT AS PARQUET;
        """
        cursor.execute(copy_query)
        conn.commit()
        
        # Fechar a conexão
        cursor.close()
        conn.close()
        
        return {"status": "success", "message": "Dados carregados no Redshift com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))