import requests
from bs4 import BeautifulSoup
from fastapi import UploadFile
from api.utils.upfile_bucketS3 import upload_file
import io
import pandas as pd

async def fetch_data(url:str, file_name:str):
    response = requests.get(url)
    if response.status_code == 200:
       # Cria um objeto BytesIO em memória com o conteúdo do arquivo
        file_content = io.BytesIO(response.content)
        print("Arquivo baixado com sucesso!")
        
        try:
           # Detecta o delimitador automaticamente
            delimiters = [';', '\t']
            df = None
            for delimiter in delimiters:
                file_content.seek(0)  # Reseta o ponteiro do arquivo para o início
                try:
                    df = pd.read_csv(file_content, delimiter=delimiter, on_bad_lines='warn')
                    if len(df.columns) > 1:  # Verifica se o DataFrame tem mais de uma coluna
                        break
                except Exception as e:
                    print(f"Erro ao tentar ler com delimitador '{delimiter}': {e}")
            
            # Verifica se o DataFrame foi lido corretamente
            if len(df.columns) == 1:
                print("Aviso: O DataFrame foi lido com apenas uma coluna. Verifique o delimitador.")

            
            # Converte o DataFrame em um arquivo Parquet em memória
            parquet_buffer = io.BytesIO()
            df.to_parquet(parquet_buffer, index=False)
            parquet_buffer.seek(0)
            
            # Cria um objeto UploadFile em memória com o arquivo Parquet
            upload_file_obj = UploadFile(file=parquet_buffer, filename=file_name)
            
            # Upload do arquivo Parquet para o S3
            upload_response = await upload_file(upload_file_obj)
            print(upload_response)
            
            # Faz o parse do conteúdo original usando BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        except pd.errors.ParserError as e:
            print(f"Erro ao processar o arquivo CSV: {e}")
            return None
    else:
        return None
    
