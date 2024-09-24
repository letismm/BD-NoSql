use('BlogGi')

db.posts.updateOne(
    { "_id": "post_001" },
    { $set: { "conteudo": "Estou estudando NoSQL, muito interessante! Aprendendo bastante." } }
);

db.posts.find(
    { "_id": "post_001" }
)

db.usuarios.updateOne(
    { "_id": "user_001" },
    { $set: { "nome": "João Silva Pereira" } }
);

db.usuarios.findOne({
    "_id": "user_001"
});
