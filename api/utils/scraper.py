import requests
from bs4 import BeautifulSoup
from fastapi import UploadFile
from api.utils.upfile_bucketS3 import upload_file
import io
import pandas as pd
import re

async def fetch_data(url: str, file_name: str):
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
                
            # Tratar Dataframe
            
            # Nomear todas as colunas para minúsculas
            df.columns = df.columns.str.lower()
            
            # Verifica se existe coluna id, se sim remover
            if 'id' in df.columns:
                df = df.drop(columns=['id'])
                
            # Identificar colunas que terminam com '.1' e renomeá-las para 'valor'
            df.columns = ['valor' if col.endswith('.1') else col for col in df.columns]
            if 'valor' in df.columns:        
                # Identificar colunas que não são anos
                id_vars = [col for col in df.columns if not col.isdigit() and col != 'valor']
                # Criar DataFrame a partir de df com apenas colunas id_vars e valor
                df_valores = df[id_vars + ['valor']]
                        
                # Usar melt para transformar as colunas de anos em linhas
                df_quantidade = df.melt(id_vars=id_vars, var_name='ano', value_name='quantidade')
                df_valor = df_valores.melt(id_vars=id_vars, var_name='ano', value_name='valores')
                df_valor = df_valor['valores']
                
                # Filtrar apenas as linhas onde 'ano' é um número
                df_quantidade = df_quantidade[df_quantidade['ano'].str.isdigit()]
                
                df_quantidade = df_quantidade.reset_index(drop=True)
                
                # Converte a coluna 'quantidade' para numérico
                df_quantidade['quantidade'] = pd.to_numeric(df_quantidade['quantidade'], errors='coerce')
                
                # Opcional: Preenche valores NaN com 0 ou outro valor padrão
                df_quantidade['quantidade'] = df_quantidade['quantidade'].fillna(0)
                
                # Combinar os DataFrames de quantidade e valor
                df_final = pd.merge(df_quantidade, df_valor, left_index=True, right_index=True)
                
                # Reorganizar as colunas dinamicamente
                df_final = df_final[id_vars + ['quantidade', 'ano','valores']]
            else:
                # Identificar colunas que não são anos
                id_vars = [col for col in df.columns if not col.isdigit()]
                
                # Usar melt para transformar as colunas de anos em linhas
                df_final = df.melt(id_vars=id_vars, var_name='ano', value_name='quantidade')
                
                # Converte a coluna 'quantidade' para numérico
                df_final['quantidade'] = pd.to_numeric(df_final['quantidade'], errors='coerce')
                
                # Opcional: Preenche valores NaN com 0 ou outro valor padrão
                df_final['quantidade'] = df_final['quantidade'].fillna(0)
                               
            
            
            
            # Converte o DataFrame em um arquivo Parquet em memória
            parquet_buffer = io.BytesIO()
            df_final.to_parquet(parquet_buffer, index=False)
            parquet_buffer.seek(0)
            
            # Cria um objeto UploadFile em memória com o arquivo Parquet
            upload_file_obj = UploadFile(file=parquet_buffer, filename=file_name)
            
            # Upload do arquivo Parquet para o S3
            upload_response = await upload_file(upload_file_obj)
            if upload_response['status'] == 'success':
                print("Arquivo enviado ao Data Lake com sucesso!")
            print(upload_response)
            
            # Faz o parse do conteúdo original usando BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        except pd.errors.ParserError as e:
            print(f"Erro ao processar o arquivo CSV: {e}")
            return None
    else:
        return None