from fastapi import FastAPI, HTTPException
from db import collection_usuario, collection_post, collection_comentario
from pydantic import BaseModel
from bson import ObjectId
from typing import List
import redis.asyncio as redis
from datetime import datetime

from neo4j import GraphDatabase
import redis

URI = "neo4j+s://c849aa85.databases.neo4j.io"
AUTH = ("neo4j", "MhAB8ceKBh1rZt3YsImFHv8Z7V1PNpIW3YZq-oOleaQ")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection established.")

redis_client = redis.Redis(
  host='redis-12766.c308.sa-east-1-1.ec2.redns.redis-cloud.com',
  port=12766,
  password='XEQnp0K0HmDM4k64fAJ9cOOhEU1zgvzO')

app = FastAPI()

class User(BaseModel):
    nome: str
    email: str
    periodo: int

async def init_count_min_sketch():
    await redis_client.execute_command('CMS.INITBYDIM', 'post_views', 2000, 7)

# Increment post view count
async def increment_post_view(post_id: str):
    await redis_client.execute_command('CMS.INCRBY', 'post_views', post_id, 1)

# Get view count for a post
async def get_post_view_count(post_id: str) -> int:
    count = await redis_client.execute_command('CMS.QUERY', 'post_views', post_id)
    return count[0] if count else 0

# Top-K to track most commented posts
async def init_top_k():
    await redis_client.execute_command('TOPK.RESERVE', 'top_commented_posts', 10, 2000, 7, 0.9)

# Increment comment count for a post in Top-K
async def increment_post_comment_count(post_id: str):
    await redis_client.execute_command('TOPK.INCRBY', 'top_commented_posts', post_id, 1)

# Get Top-K most commented posts
async def get_top_commented_posts():
    return await redis_client.execute_command('TOPK.LIST', 'top_commented_posts')

# Route to increment and fetch post views
@app.post("/posts/{post_id}/view")
async def view_post(post_id: str):
    await increment_post_view(post_id)
    view_count = await get_post_view_count(post_id)
    return {"post_id": post_id, "view_count": view_count}

# Route to increment and fetch most commented posts
@app.post("/posts/{post_id}/comment")
async def comment_post(post_id: str):
    await increment_post_comment_count(post_id)
    top_posts = await get_top_commented_posts()
    return {"top_commented_posts": top_posts}

async def gera_id_usuario():
    user_count = await collection_usuario.count_documents({})
    user_number = user_count + 1
    return f"user_{user_number:03d}"

# Chave-valor: Armazenar o último login de um usuário
@app.post("/usuarios/{user_id}/login")
async def login_usuario(user_id: str):
    login_time = datetime.now().isoformat()
    # Armazenar a última vez que o usuário fez login
    redis_client.mset({
      'user': user_id,
      'last_login': login_time
    })
    return {"message": f"Login registrado para o usuário {user_id} em {login_time}"}

@app.get("/usuarios/last_login")
async def get_last_login():
    user_id, last_login = redis_client.mget("user", "last_login")
    if user_id and last_login:
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


--- Neo4j

from neo4j import GraphDatabase

uri = "neo4j+s://21f60417.databases.neo4j.io"
AUTH = ("neo4j", "ma0OtCJc5DT7KAmue6rouFQDWnEECPbKsbAzqYkoOBE")

driver = GraphDatabase.driver(uri, auth=AUTH)

with driver.session() as session:
  # Cria os nós dos usuários
  session.run("CREATE (u1:Usuario {user_id: 'user_001', nome: 'João', email: 'joao@example.com', periodo: 3, data_entrada: '2024-08-01'})")
  session.run("CREATE (u2:Usuario {user_id: 'user_002', nome: 'Maria', email: 'maria@example.com', periodo: 2, data_entrada: '2024-08-02'})")

  # Cria o nó de post
  session.run("CREATE (p1:Post {post_id: 'post_001', titulo: 'Primeiro Post', conteudo: 'Conteúdo do primeiro post', data_criacao: '2024-08-10'})")

  # Cria o nó comentário
  session.run("CREATE (c1:Comentario {comentario_id: 'comment_001', conteudo: 'Ótimo post!', data_criacao: '2024-08-15'})")
  
  # Relacionar Usuários com Posts (Ex: Usuário João criou um post)
  session.run("""
        MATCH (u1:Usuario {user_id: 'user_001'}), (p1:Post {post_id: 'post_001'})
        CREATE (u1)-[:USUARIO_CRIOU_POST]->(p1)
    """)

  # Relacionar Usuário com Post comentado (Ex: Usuário Maria comentou no post do João)
  session.run("""
        MATCH (u2:Usuario {user_id: 'user_002'}), (p1:Post {post_id: 'post_001'})
        CREATE (u2)-[:USUARIO_COMENTOU_POST]->(p1)
    """)
  
driver.close()


--- consultando

def execute_query(query):
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# Consultas Cypher
queries = {
    "Todos os usuários": """
        MATCH (u:Usuario)
        RETURN u.user_id AS user_id, u.nome AS nome, u.email AS email, u.periodo AS periodo, u.data_entrada AS data_entrada
    """,
    "Posts e autores": """
        MATCH (u:Usuario)-[:USUARIO_CRIOU_POST]->(p:Post)
        RETURN u.nome AS Autor, p.titulo AS Titulo_Post, p.data_criacao AS Data_Criacao
    """,
    "Comentários nos posts": """
        MATCH (u:Usuario)-[:USUARIO_COMENTOU_POST]->(p:Post)
        MATCH (c:Comentario)-[:USUARIO_COMENTOU_POST]->(p)
        RETURN u.nome AS Comentador, c.conteudo AS Comentario, p.titulo AS Post, p.data_criacao AS Data_Post
    """,
    "Usuários que comentaram posts de outros usuários": """
        MATCH (u1:Usuario)-[:USUARIO_COMENTOU_POST]->(p:Post)<-[:USUARIO_CRIOU_POST]-(u2:Usuario)
        WHERE u1 <> u2
        RETURN u1.nome AS Usuario_Comentador, u2.nome AS Usuario_Autor, p.titulo AS Titulo_Post
    """
}

# Executar consultas e imprimir resultados
for descricao, query in queries.items():
    print(f"\n--- {descricao} ---")
    resultado = execute_query(query)
    for record in resultado:
        print(record)

# Fechar a conexão com o Neo4j
driver.close()
