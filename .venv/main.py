from fastapi import FastAPI, HTTPException
from app.db import collection_usuario, collection_post, collection_comentario
from pydantic import BaseModel
from bson import ObjectId
from typing import List
import redis.asyncio as redis
from datetime import datetime

redis_client = redis.Redis(
    host='memcached-14411.c308.sa-east-1-1.ec2.redns.redis-cloud.com',
    port=14411,
    password='',
    decode_responses=True
)

app = FastAPI()

class User(BaseModel):
    nome: str
    email: str
    periodo: int

async def gera_id_usuario():
    user_count = await collection_usuario.count_documents({})
    user_number = user_count + 1
    return f"user_{user_number:03d}"

# Chave-valor: Armazenar o último login de um usuário
@app.post("/usuarios/{user_id}/login")
async def login_usuario(user_id: str):
    login_time = datetime.now().isoformat()
    # Armazenar a última vez que o usuário fez login
    await redis_client.mset({
      'user': user_id,
      'last_login': login_time
    })
    return {"message": f"Login registrado para o usuário {user_id} em {login_time}"}

@app.get("/usuarios/{user_id}/last_login")
async def get_last_login(user_id: str):
    last_login = await redis_client.get(f"user:{user_id}:last_login")
    if last_login:
      return {"user_id": user_id, "last_login": last_login.decode("utf-8")}
    raise HTTPException(status_code=404, detail="Login não encontrado para o usuário")

@app.post("/usuarios/")
async def criar_usuario(user: User):
    user_id = await gera_id_usuario()
    user_dict = user.model_dump()
    user_dict['_id'] = user_id
    user_dict['data_entrada'] = datetime.now().isoformat()
    result = await collection_usuario.insert_one(user_dict)
    return {"id": str(result.inserted_id), "mensagem":"Usuário Criado com Sucesso"}

@app.get("/usuarios/")
async def listar_usuarios():
    usuarios = []
    async for usuario in collection_usuario.find():
        usuario["_id"] = str(usuario["_id"])  # Converter ObjectId para string
        usuarios.append(usuario)
    return usuarios

@app.put("/usuarios/{user_id}")
async def atualizar_usuario(user_id: str, user: User):
    update_result = await collection_usuario.update_one(
        {"_id": user_id},{"$set":user.model_dump()}
    )

    if update_result.modified_count == 1:
        return {"message": "Usuário atualizado com sucesso"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.delete("/usuarios/{user_id}")
async def deletar_usuario(user_id: str):
    delete_result = await collection_usuario.delete_one({"_id": user_id})

    if delete_result.deleted_count == 1:
        return {"message": "Usuário deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.get("/usuarios/{user_id}")
async def get_user(user_id: str):
    user = await collection_usuario.find_one({"_id": user_id})

    if user is not None:
        return user
    
    raise HTTPException(status_code=404, detail="Usuário não encontrado")


@app.get("/usuarios-participativos/")
async def get_usuarios_participativos():
    pipeline = [
  {
    "$lookup":{
      "from": "posts",
      "localField": "id_post",
      "foreignField": "_id",
      "as": "post_info"
    }
  },
  {
    "$unwind":"$post_info"
  },
  {
    "$match":{
      "$expr":{
        "$ne":["$id_usuario", "$post_info.id_usuario"]
      }    
    }
  },
  {
    "$group":{
      "_id": "$id_usuario",
      "total_comentarios":{
        "$sum":1
      }
    }
  },
  {
    "$sort":{
      "total_comentarios":-1
    }
  }
]

    resultado = await collection_comentario.aggregate(pipeline).to_list(length=10)
    return {"usuarios-mais-participativos": resultado}