from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    id: Optional[int] = None
    username: str
    admin: bool = False
    
    class Config:
        from_attributes = True
    
class UsuarioCreate(UsuarioBase):
    password: str
        
class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    admin: Optional[bool] = None