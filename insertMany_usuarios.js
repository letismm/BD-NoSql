use('BlogGi')

db.getCollection('usuario').insertMany([
    {
        "_id": "user_001",
        "nome": "João Silva",
        "email": "joao.silva@example.com",
        "data_entrada": "2022-03-01",
        "periodo": 4
    },
    {
        "_id": "user_002",
        "nome": "Maria Oliveira",
        "email": "maria.oliveira@example.com",
        "data_entrada": "2021-09-15",
        "periodo": 6
    },
    {
        "_id": "user_003",
        "nome": "Pedro Souza",
        "email": "pedro.souza@example.com",
        "data_entrada": "2023-02-20",
        "periodo": 2
    }
])