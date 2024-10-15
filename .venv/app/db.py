from motor.motor_asyncio import AsyncIOMotorClient
import json


with open(".venv/config.json") as config_file:
    config = json.load(config_file)

MONGO_USER = config['MONGO_USER']
MONGO_PASSWORD = config['MONGO_PASSWORD']

MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@blog-gi.he0jy.mongodb.net/?retryWrites=true&w=majority&appName=Blog-Gi"
client = AsyncIOMotorClient(MONGO_URI)
db = client.BlogGi

collection_usuario = db['usuario']
collection_post = db['posts']
collection_comentario = db['comentarios']