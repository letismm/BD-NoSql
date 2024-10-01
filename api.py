from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from typing import List

# Conectar ao MongoDB Atlas
MONGO_URI = "mongodb+srv://georgealbuquerque:Ga!pitoko1@Blog-Gi.mongodb.net/Blog-Gi?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGO_URI)
db = client.Blog-Gi  # Nome do banco de dados

app = FastAPI()

# Modelos para validar os dados da API
class UserModel(BaseModel):
    nome: str
    email: str
    data_entrada: str
    periodo: int

class PostModel(BaseModel):
    id_usuario: str
    conteudo: str
    timestamp: str
    interacoes: int

class CommentModel(BaseModel):
    id_post: str
    id_usuario: str
    conteudo: str
    timestamp: str
    id_comentario_pai: str = None

# Função para converter ObjectId do MongoDB para string
def serialize_id(document):
    document["_id"] = str(document["_id"])
    return document

# Rota para criar um novo usuário
@app.post("/users", response_model=UserModel)
async def create_user(user: UserModel):
    result = await db["users"].insert_one(user.dict())
    user_created = await db["users"].find_one({"_id": result.inserted_id})
    return serialize_id(user_created)

# Rota para listar todos os usuários
@app.get("/users", response_model=List[UserModel])
async def list_users():
    users = await db["users"].find().to_list(100)
    return [serialize_id(user) for user in users]

# Rota para criar um post
@app.post("/posts", response_model=PostModel)
async def create_post(post: PostModel):
    result = await db["posts"].insert_one(post.dict())
    post_created = await db["posts"].find_one({"_id": result.inserted_id})
    return serialize_id(post_created)

# Rota para listar todos os posts
@app.get("/posts", response_model=List[PostModel])
async def list_posts():
    posts = await db["posts"].find().to_list(100)
    return [serialize_id(post) for post in posts]

# Rota para criar um comentário
@app.post("/comments", response_model=CommentModel)
async def create_comment(comment: CommentModel):
    result = await db["comments"].insert_one(comment.dict())
    comment_created = await db["comments"].find_one({"_id": result.inserted_id})
    return serialize_id(comment_created)

# Rota para listar todos os comentários
@app.get("/comments", response_model=List[CommentModel])
async def list_comments():
    comments = await db["comments"].find().to_list(100)
    return [serialize_id(comment) for comment in comments]
