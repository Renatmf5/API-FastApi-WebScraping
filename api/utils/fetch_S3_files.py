import boto3
import pandas as pd
from fastapi import HTTPException
from typing import List
from core.config import settings
from pydantic import BaseModel
import os

s3_client = boto3.client('s3')
bucket_name = settings.BUCKET_NAME  # Substitua pelo nome do seu bucket

class DataResponse(BaseModel):
    columns: List[str]
    data: List[List[str]]
    
    
class TablesResponse(BaseModel):
    tables: List[str]

def list_files_in_s3(prefix: str) -> TablesResponse:
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        files = [os.path.splitext(os.path.basename(content['Key']))[0] for content in response.get('Contents', [])]
        return TablesResponse(tables=files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def read_parquet_from_s3(file_key: str, year_filter: str) -> DataResponse:
    try:
        # Ler o arquivo .parquet diretamente do S3 usando pandas
        s3_path = f's3://{bucket_name}/Lake/{file_key}.parquet'
        df = pd.read_parquet(s3_path)
        if year_filter:
            df = df[df['ano'] == year_filter]

        # Converter DataFrame para lista de listas
        columns = df.columns.tolist()
        data = df.astype(str).values.tolist()

        return DataResponse(columns=columns, data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Exemplo de uso
def list_tables_from_s3() -> TablesResponse:
    return list_files_in_s3('Lake/')  # Prefixo para os arquivos no S3

def fetch_data_from_s3(file_key: str, year_filter: str) -> DataResponse:
    return read_parquet_from_s3(file_key, year_filter)