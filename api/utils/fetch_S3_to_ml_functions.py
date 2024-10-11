import boto3
import pandas as pd
from fastapi import HTTPException
from core.config import settings

s3_client = boto3.client('s3')
bucket_name = settings.BUCKET_NAME  # Substitua pelo nome do seu bucket
    
def trat_parquet_from_s3(file_key: str):
    try:
        # Ler o arquivo .parquet diretamente do S3 usando pandas
        s3_path = f's3://{bucket_name}/Lake/{file_key}.parquet'
        df = pd.read_parquet(s3_path)
        
        # Filtrar linhas onde a coluna "Produto" esteja com letras maiúsculas
        if file_key in ["Producao", "Comercio"]:
            df = df[df['produto'].str.isupper()]
            # excluir linhas duplicadas e zeradas
            df = df.drop_duplicates()
            df = df[df['quantidade'] > 0]
            
            # Agrupar por ano e somar as quantidades
            df_grouped = df.groupby('ano').agg({'quantidade': 'sum'}).reset_index()
            df_grouped.rename(columns={'quantidade': 'total_quantidade'}, inplace=True)
            
            # Fazer merge do DataFrame original com o DataFrame agrupado
            df = df.merge(df_grouped, on='ano', how='left')
                
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))