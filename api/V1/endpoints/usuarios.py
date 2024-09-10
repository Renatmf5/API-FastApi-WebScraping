from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from core.auth import get_current_user, get_password_hash, autenticar_usuario, create_access_token, get_user
from core.database import get_session
from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioBase, UsuarioCreate, UsuarioUpdate


router = APIRouter()

# GET logado
@router.get("/logado", response_model=UsuarioBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    if not usuario_logado:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    return usuario_logado

# POST login
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    usuario = autenticar_usuario(form_data.username, form_data.password, db)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = create_access_token(data={"sub": usuario.username})
    return {"access_token": token, "token_type": "bearer"}

# POST / Sign up
@router.post("/signup", response_model=UsuarioBase)
def signup(usuario: UsuarioCreate, db: Session = Depends(get_session)):
    valida_db_user = get_user(db, usuario.username)
    # Validar se username ja existe cadastrado na base
    if valida_db_user.username == usuario.username:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Usuário já cadastrado")
    usuario_db = UsuarioModel(username=usuario.username, 
                                    password=get_password_hash(usuario.password), 
                                    admin=usuario.admin)
    try:
        db.add(usuario_db)
        db.commit()
        db.refresh(usuario_db)
        return usuario_db
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Usuário já cadastrado")

# GET trazer todos os usuarios
@router.get("/usuarios", response_model=list[UsuarioBase])
def get_usuarios(db: Session = Depends(get_session)):
    statement = select(UsuarioModel)
    usuarios = db.exec(statement).all()
    return usuarios

# PUT alterar usuario
@router.put("/{usuario_id}", response_model=UsuarioBase, status_code=status.HTTP_202_ACCEPTED)
def put_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_session)):
    usuario_db = db.get(UsuarioModel, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    update_data = usuario.dict(exclude_unset=True)
    for key, value in update_data.items():
        print("key", key)
        print("value", value)
        setattr(usuario_db, key, value)
        if key == "password":
            setattr(usuario_db, key, get_password_hash(value))
            print("entrei aqui no password", value, get_password_hash(value))
        
    print("usuario_db", usuario_db)
    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db)
    return usuario_db