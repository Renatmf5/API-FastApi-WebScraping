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
    data = await fetch_data(settings.URL_DOWNLOAD+"/Comercio.csv", "Lake/Comercio.parquet")
    if data:     
        return {"status": "Dados de comercialização enviados ao Data-Lake com sucesso"}
    else:
        return {"status": "Falha ao extrair dados de comercialização"}