from fastapi import APIRouter
from api.utils.scraper import fetch_data
from core.config import settings

router = APIRouter()

@router.get("/download-arquivo")
def download_arquivo():
    data = fetch_data(settings.URL_DOWNLOAD+"/Producao.csv", "Producao.csv")
    if data:
        # extrair dados e fazer o download na pasta local do projeto        
        return {"status": "Dados de produção extraídos com sucesso"}
    else:
        return {"status": "Falha ao extrair dados de produção"}