from fastapi import APIRouter
from core.proxy import request
from core.exceptions import HTTP_E401,HTTP_E404
from pydantic import BaseModel,Field
from typing import Optional,Literal,Union,Dict
from core.utils import generate_random_string,str_to_bytes,bytes_to_str
from models.Procedure import Procedure
from models.ProcedureInfo import ProcedureInfo
procedure_router = APIRouter(prefix="/procedure")

class ProcedurePostSchema(BaseModel):
    procedure_raw:str
    procedure_name:Optional[str] = Field(default=generate_random_string())
    procedure_type:Literal["script","package"] = Field(default="package")   #Cases for type: Execute Type:[MOUNT ONLY,EXECUTE ONLY,MOUNT AND EXECUTE]
    procedure_encrypt_type:Optional[Literal["AES","SM4"]] = Field(default="AES")
    procedure_decrypt_key:str
    procedure_extra:Optional[str]

###########################
#    PROCEURE CURD        # 
#    PROCEDURE INFO CURD  #  UNION
###########################
    
