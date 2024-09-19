# BD-NoSql

**Rede social para Gestão da Informação**

Authors: Letícia Machado e George Lucas

A rede social para o curso de Gestão da Informação tem como objetivo reunir os estudantes do curso assim como obter apoio durante a graduação. Aqui será possível interagir com os estudantes de diferentes períodos, cada usuário possui seu cadastro e pode realizar publicações como: uma lista de exercícios resolvida com comentários para auxiliar outros alunos, um artigo lido que achou interessante publicar, uma questão de cálculo em dúvida pedindo ajuda de outros usuários, enfim. Cada publicação permite que os usuários comentem, e que comentem em outros comentários.

O Sistema de Comentários para um Blog irá permitir que os usuários publiquem comentários em postagens específicas. Os comentários devem ser associados a uma postagem, conter o nome do autor, o texto do comentário, data/hora da criação, e podem permitir respostas entre os comentários, criando conversas encadeadas. O sistema deverá ser eficiente na leitura de grandes volumes de dados (vários comentários por postagem) e flexível para gerenciar metadados de comentários e respostas.

A escolha de um banco de dados NoSQL baseado em modelo de **documentos**, é ideal para essa aplicação devido à flexibilidade e simplicidade no armazenamento de dados sem a necessidade de estruturas rígidas como tabelas e relações fixas. Utilizaremos o **FIREBASE** como estrutura para o banco de dados NoSql, oferece sincronização de dados em tempo real, ideal para posts e comentários que devem ser atualizados instantaneamente. Ele simplifica o gerenciamento de autenticação, segurança e escalabilidade automática, eliminando a necessidade de backend manual. Além disso, fornece armazenamento para mídia e funções serverless para lógica de backend, permitindo o rápido desenvolvimento de aplicações robustas e escaláveis.

Comentários podem ter diferentes metadados (nome, email, data, respostas) que podem variar de um comentário para outro. O modelo de documentos armazena dados em formatos como JSON, permitindo essa flexibilidade, onde cada documento pode ter sua própria estrutura podendo adicionar novos campos (ex. moderado, oculto, editado) facilmente sem modificar uma tabela inteira ou impactar outras partes do sistema. Em um blog social, postagens podem ter milhares de comentários, e as consultas podem aumentar exponencialmente. O modelo de documentos permite armazenar todos os comentários de uma postagem juntos, em um documento único ou em coleções, melhorando o desempenho de leitura e escrita.


**Estrutura do Documento em JSON**:

- Coleção usuários:
{
  "_id": "123", 
  "nome": "João Silva",
  "email": "joao.silva@email.com",
  "data_entrada": "2024-01-15",
  "curso": "Ciência da Computação"
}

- Coleção posts:
{
  "_id": "456",
  "conteudo": "Esse é o conteúdo do post",
  "id_usuario": "123",
  "interacoes": 10,
  "timestamp": "2024-09-15T14:30:00Z"
}

- Coleção comentários:
{
  "_id": "789",
  "id_post": "456",
  "conteudo": "Esse é o primeiro comentário",
  "timestamp": "2024-09-15T15:00:00Z",
  "id_comentario_pai": null
}
{
  "_id": "790",
  "id_post": "456",
  "conteudo": "Esse é um comentário em resposta ao primeiro comentário",
  "timestamp": "2024-09-15T16:00:00Z",
  "id_comentario_pai": "789"
}


**Relação entre a coleção de documentos**:

![Diagrama Blog drawio](https://github.com/user-attachments/assets/f1210768-f708-4f91-9bf2-15e8d947b84d)
