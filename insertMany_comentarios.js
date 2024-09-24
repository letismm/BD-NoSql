use("BlogGi")

db.getCollection('comentarios').insertMany([
    {
        "_id": "comment_001",
        "id_post": "post_001",
        "id_usuario": "user_002",  // Maria Oliveira comentou
        "conteudo": "Também estou gostando bastante, João!",
        "timestamp": "2024-09-20T11:00:00Z",
        "id_comentario_pai": null
    },
    {
        "_id": "comment_002",
        "id_post": "post_002",
        "id_usuario": "user_003",  // Pedro Souza comentou
        "conteudo": "Recomendo focar em índices e sharding.",
        "timestamp": "2024-09-21T15:00:00Z",
        "id_comentario_pai": null
    },
    {
        "_id": "comment_003",
        "id_post": "post_002",
        "id_usuario": "user_001",  // João Silva respondeu
        "conteudo": "Valeu pela dica, Maria!",
        "timestamp": "2024-09-21T16:00:00Z",
        "id_comentario_pai": "comment_002"
    },
    {
        "_id": "comment_004",
        "id_post": "post_003",
        "id_usuario": "user_001",  // João Silva comentou
        "conteudo": "Parabéns Pedro! Qual foi o maior desafio?",
        "timestamp": "2024-09-22T09:00:00Z",
        "id_comentario_pai": null
    },
    {
        "_id": "comment_005",
        "id_post": "post_003",
        "id_usuario": "user_003",  // Pedro Souza respondeu
        "conteudo": "Obrigado! O mais difícil foi configurar a replicação.",
        "timestamp": "2024-09-22T10:00:00Z",
        "id_comentario_pai": "comment_004"
    }
])