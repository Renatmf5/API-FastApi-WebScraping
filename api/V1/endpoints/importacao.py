from fastapi import APIRouter,Depends
from api.utils.scraper import fetch_data
from core.config import settings
from core.auth import get_current_user
from models.usuario_model import UsuarioModel

router = APIRouter()

@router.get("/download-arquivo")
def download_arquivo(usuario_logado: UsuarioModel = Depends(get_current_user)):
    if not usuario_logado.admin:
        return {"status": "Usuário não autorizado"}
    vinhos_de_mesa = fetch_data(settings.URL_DOWNLOAD+"/ImpVinhos.csv", "ImpVinhos.csv")
    espumantes = fetch_data(settings.URL_DOWNLOAD+"/ImpEspumantes.csv", "ImpEspumantes.csv")
    Uvas_frescas = fetch_data(settings.URL_DOWNLOAD+"/ImpFrescas.csv", "ImpFrescas.csv")
    Uvas_passas = fetch_data(settings.URL_DOWNLOAD+"/ImpPassas.csv", "ImpPassas.csv")
    Suco_uva = fetch_data(settings.URL_DOWNLOAD+"/ImpSuco.csv", "ImpSuco.csv")
    if vinhos_de_mesa and espumantes and Uvas_frescas and Uvas_passas and Suco_uva:       
        return {"status": "Dados de produção extraídos com sucesso"}
    else:
        return {"status": "Falha ao extrair dados de produção"}
