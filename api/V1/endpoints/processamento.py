from fastapi import APIRouter, Depends
from api.utils.scraper import fetch_data
from core.config import settings
from core.auth import get_current_user
from models.usuario_model import UsuarioModel

router = APIRouter()

@router.get("/download-arquivo")
def download_arquivos(usuario_logado: UsuarioModel = Depends(get_current_user)):
    if not usuario_logado.admin:
        return {"status": "Usuário não autorizado"}
    Viniferas_data = fetch_data(settings.URL_DOWNLOAD+"/ProcessaViniferas.csv", "ProcessaViniferas.csv")
    Americanas_data = fetch_data(settings.URL_DOWNLOAD+"/ProcessaAmericanas.csv", "ProcessaAmericanas.csv")
    Mesa_data = fetch_data(settings.URL_DOWNLOAD+"/ProcessaMesa.csv", "ProcessaMesa.csv")
    SemClass_data = fetch_data(settings.URL_DOWNLOAD+"/ProcessaSemclass.csv", "ProcessaSemclass.csv")
    if Viniferas_data and Americanas_data and Mesa_data and SemClass_data:     
        return {"status": "Dados de produção extraídos com sucesso"}
    else:
        return {"status": "Falha ao extrair dados de produção"}