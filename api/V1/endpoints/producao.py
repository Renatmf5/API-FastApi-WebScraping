from fastapi import APIRouter, Depends
from api.utils.scraper import fetch_data
from core.config import settings
from core.auth import get_current_user
from models.usuario_model import UsuarioModel

router = APIRouter()

@router.get("/download-arquivo")
async def download_arquivo(usuario_logado: UsuarioModel = Depends(get_current_user)):
    # Valida se usuario_logado atributo é admin true
    if not usuario_logado.admin:
        return {"status": "Usuário não autorizado"}
    data = await fetch_data(settings.URL_DOWNLOAD+"/Producao.csv", "Lake/Producao.parquet")
    if data:
        # extrair dados e fazer o download no data lake        
        return {"status": "Dados de produção enviados ao Data-Lake com sucesso"}
    else:
        return {"status": "Falha ao extrair dados de produção"}