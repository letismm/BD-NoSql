
use('BlogGi')

// criação do índice de texto para o conteúdo:

db.posts.createIndex({ conteudo: "text" })

// busca do índice:

db.posts.find({ $text: { $search: "NoSQL" } })


// criação do índice por nome (se houver buscas frequentes por nomes de usuários):

db.usuario.createIndex({ nome: 1 })


// Índice Composto em id_post e timestamp (para buscas de comentários de um post ordenados por data)

db.comentarios.createIndex({ id_post: 1, timestamp: 1 })