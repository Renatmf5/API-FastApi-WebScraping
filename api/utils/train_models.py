import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os
import numpy as np

def train(df: pd.DataFrame, file_key: str):
    # Lista de produtos
    if file_key in ["Producao", "Comercio"]:
        produtos = df['produto'].unique()

        # Dicionário para armazenar os modelos e previsões
        modelos = {}
        
        # Listas para armazenar os scores
        train_scores = []
        test_scores = []

        # Pré-processamento e treinamento do modelo para cada produto
        for produto in produtos:
            df_produto = df[df['produto'] == produto]
            
            # Definir variáveis independentes (X) e dependentes (y)
            X = df_produto[['ano']]
            y = df_produto['quantidade']
            
            # Dividir os dados em conjuntos de treino e teste
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Treinar o modelo de Regressão Linear
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            # Coeficiente de Determinação dados de treino
            train_score = round(model.score(X_train, y_train),2)
            test_score = round(model.score(X_test, y_test),2)
            
            # Adicionar scores às listas, ignorando NaN
            if not np.isnan(train_score):
                train_scores.append(train_score)
            if not np.isnan(test_score):
                test_scores.append(test_score)
                        
            # Treinar o modelo de Regressão Linear
            model_export = LinearRegression()
            model_export.fit(X, y)
            
            # Armazenar o modelo treinado
            modelos[produto] = model_export
            
             # Exportar o modelo treinado
            model_path = os.path.join("models", "ml_models", f'model_{produto}.pkl')
            joblib.dump(model_export, model_path)
        
        # Calcular a média dos scores, ignorando NaN
        mean_train_score = np.nanmean(train_scores)
        mean_test_score = np.nanmean(test_scores)
            
        # Criar JSON com as médias dos scores
        scores_json = {
            "mean_train_score": round(mean_train_score, 2),
            "mean_test_score": round(mean_test_score, 2),
            "categoria": file_key
        }

        return scores_json