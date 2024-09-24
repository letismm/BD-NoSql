use('BlogGi')

db.comentarios.deleteOne({ "_id": "comment_001" });

db.comentarios.find({ "_id": "comment_001" });