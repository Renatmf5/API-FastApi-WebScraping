from fastapi import APIRouter,Depends
from api.utils.scraper import fetch_data
from core.config import settings
from core.auth import get_current_user
from models.usuario_model import UsuarioModel

router = APIRouter()

@router.get("/download-arquivo")
async def download_arquivo(usuario_logado: UsuarioModel = Depends(get_current_user)):
    if not usuario_logado.admin:
        return {"status": "Usuário não autorizado"}
    vinhos_de_mesa = await fetch_data(settings.URL_DOWNLOAD+"/ImpVinhos.csv", "Bronze/ImpVinhos.parquet")
    espumantes = await fetch_data(settings.URL_DOWNLOAD+"/ImpEspumantes.csv", "Bronze/ImpEspumantes.parquet")
    Uvas_frescas = await fetch_data(settings.URL_DOWNLOAD+"/ImpFrescas.csv", "Bronze/ImpFrescas.parquet")
    Uvas_passas = await fetch_data(settings.URL_DOWNLOAD+"/ImpPassas.csv", "Bronze/ImpPassas.parquet")
    Suco_uva = await fetch_data(settings.URL_DOWNLOAD+"/ImpSuco.csv", "Bronze/ImpSuco.parquet")
    if vinhos_de_mesa and espumantes and Uvas_frescas and Uvas_passas and Suco_uva:       
        return {"status": "Dados de produção extraídos com sucesso"}
    else:
        return {"status": "Falha ao extrair dados de produção"}
