from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from typing import List
from datetime import datetime
import json


with open(".venv/config.json") as config_file:
    config = json.load(config_file)

MONGO_USER = config['MONGO_USER']
MONGO_PASSWORD = config['MONGO_PASSWORD']

MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@blog-gi.he0jy.mongodb.net/?retryWrites=true&w=majority&appName=Blog-Gi"
client = AsyncIOMotorClient(MONGO_URI)
db = client.BlogGi

app = FastAPI()

collection_usuario = db['usuario']
collection_post = db['posts']
collection_comentario = db['comentarios']

class User(BaseModel):
    nome: str
    email: str
    data_entrada: str
    periodo: int

async def gera_id_usuario():
    user_count = await collection_usuario.count_documents({})
    user_number = user_count + 1
    return f"user_{user_number:03d}"

@app.post("/usuarios/")
async def criar_usuario(user: User):
    user_id = await gera_id_usuario()
    user_dict = user.model_dump()
    user_dict['_id'] = user_id
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