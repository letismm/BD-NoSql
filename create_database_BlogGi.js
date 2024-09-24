const database = 'BlogGi'
const collection = 'usuario'

db = db.getSiblingDB(database) /* Usado para navegar entre banco de dados na mesma conexão. 
                                O banco de dados não precisa existir previamente. Se ele não existir, 
                                MongoDB o criará automaticamente quando um documento ou coleção for inserido.*/

print(db.getCollectionNames())