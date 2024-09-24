use('BlogGi')

db.getCollection('posts').insertMany([
    {
        "_id": "post_001",
        "id_usuario": "user_001",
        "conteudo": "Estou estudando NoSQL, muito interessante!",
        "timestamp": "2024-09-20T10:30:00Z",
        "interacoes": 15
    },
    {
        "_id": "post_002",
        "id_usuario": "user_002",
        "conteudo": "Alguém tem dicas de como melhorar o desempenho em MongoDB?",
        "timestamp": "2024-09-21T14:15:00Z",
        "interacoes": 30
    },
    {
        "_id": "post_003",
        "id_usuario": "user_003",
        "conteudo": "Acabei de concluir meu primeiro projeto de banco de dados NoSQL!",
        "timestamp": "2024-09-22T08:45:00Z",
        "interacoes": 8
    }
])