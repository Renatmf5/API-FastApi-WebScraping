import pandas as pd
import joblib
import os
from fastapi import HTTPException


def load_model(produto: str):
    model_path = os.path.join("models", "ml_models", f'model_{produto}.pkl')
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail=f"Modelo para o produto {produto} não foi treinado.")
    return joblib.load(model_path)

def predict(data, file_key: str, anos_futuros: list):
    
    if file_key in ["Producao", "Comercio"]:    
        produtos = data['produto'].unique()
        previsoes = {}
        previsoes_df = pd.DataFrame()

        for produto in produtos:
            model = load_model(produto)
            
            # Criar DataFrame para os anos futuros
            anos_futuros_df = pd.DataFrame({'ano': anos_futuros})
            
            # Fazer previsões
            previsoes_futuras = model.predict(anos_futuros_df)
            previsoes_futuras = previsoes_futuras.astype(int)
            previsoes[produto] = previsoes_futuras.tolist()
            
            # Criar DataFrame com as previsões
            previsoes_produto_df = pd.DataFrame({
                'produto': produto,
                'ano': anos_futuros,
                'quantidade': previsoes_futuras
            })
            
            # Concatenar previsões ao DataFrame original
            previsoes_df = pd.concat([previsoes_df, previsoes_produto_df], ignore_index=True)

         # Agrupar por ano e somar as quantidades
        df_grouped = previsoes_df.groupby('ano').agg({'quantidade': 'sum'}).reset_index()
        df_grouped.rename(columns={'quantidade': 'total_quantidade'}, inplace=True)
            
        # Fazer merge do DataFrame original com o DataFrame agrupado
        previsoes_df = previsoes_df.merge(df_grouped, on='ano', how='left')
                   
        # Concatenar o DataFrame original com as previsões
        data_incrementado = pd.concat([data, previsoes_df], ignore_index=True)
        
        # Orderar por ano
        data_incrementado = data_incrementado.sort_values(by='ano').fillna(0)
        previsoes_df = previsoes_df.fillna(0)
        
        # Converter DataFrames para JSON
        data_incrementado_json = data_incrementado.to_dict(orient='records')
        previsoes_json = previsoes_df.to_dict(orient='records')
        
        return {
            "data_incrementado": data_incrementado_json,
            "previsoes": previsoes_json
        }