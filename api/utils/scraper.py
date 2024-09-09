import requests
from bs4 import BeautifulSoup

def fetch_data(url:str, file_name:str):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'./data/{file_name}', "wb") as file:
            file.write(response.content)
        print("Arquivo baixado com sucesso!")
        soup = BeautifulSoup(response.content, "html.parser")
        
        return soup
    else:
        return None
    
