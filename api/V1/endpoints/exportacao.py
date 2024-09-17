from fastapi import APIRouter, Depends
from api.utils.scraper import fetch_data
from core.config import settings
from core.auth import get_current_user
from models.usuario_model import UsuarioModel

router = APIRouter()

@router.get("/download-arquivo")
async def download_arquivo(usuario_logado: UsuarioModel = Depends(get_current_user)):
    if not usuario_logado.admin:
        return {"status": "Usuário não autorizado"}
    vinhos_de_mesa = await fetch_data(settings.URL_DOWNLOAD+"/ExpVinho.csv", "Bronze/ExpVinho.parquet")
    espumantes = await fetch_data(settings.URL_DOWNLOAD+"/ExpEspumantes.csv", "Bronze/ExpEspumantes.parquet")
    Uvas_frescas = await fetch_data(settings.URL_DOWNLOAD+"/ExpUva.csv", "Bronze/ExpUva.parquet")
    suco_de_uva = await fetch_data(settings.URL_DOWNLOAD+"/ExpSuco.csv", "Bronze/ExpSuco.parquet")
    if vinhos_de_mesa and espumantes and Uvas_frescas and suco_de_uva:      
        return {"status": "Dados de produção extraídos com sucesso"}
    else:
        return {"status": "Falha ao extrair dados de produção"}
