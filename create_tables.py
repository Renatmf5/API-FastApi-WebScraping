from sqlmodel import SQLModel
from core.database import engine
from models.usuario_model import UsuarioModel  # Importe todos os modelos que você deseja criar

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
if __name__ == "__main__":
    create_db_and_tables()