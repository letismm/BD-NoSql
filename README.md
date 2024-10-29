# BD-NoSql

**Rede social para Gestão da Informação**

Autores: Letícia Machado e George Lucas

A rede social para o curso de Gestão da Informação tem como objetivo reunir os estudantes do curso assim como obter apoio durante a graduação. Aqui será possível interagir com os estudantes de diferentes períodos, cada usuário possui seu cadastro e pode realizar publicações como: uma lista de exercícios resolvida com comentários para auxiliar outros alunos, um artigo lido que achou interessante publicar, uma questão de cálculo em dúvida pedindo ajuda de outros usuários, enfim. Cada publicação permite que os usuários comentem, e que comentem em outros comentários.

O Sistema de Comentários para um Blog irá permitir que os usuários publiquem comentários em postagens específicas. Os comentários devem ser associados a uma postagem, conter o nome do autor, o texto do comentário, data/hora da criação, e podem permitir respostas entre os comentários, criando conversas encadeadas. O sistema deverá ser eficiente na leitura de grandes volumes de dados (vários comentários por postagem) e flexível para gerenciar metadados de comentários e respostas.

A escolha de um banco de dados NoSQL baseado em modelo de **documentos**, é ideal para essa aplicação devido à flexibilidade e simplicidade no armazenamento de dados sem a necessidade de estruturas rígidas como tabelas e relações fixas. Utilizaremos o **MongoDB** como estrutura para o banco de dados NoSql, oferece sincronização de dados em tempo real, ideal para posts e comentários que devem ser atualizados instantaneamente.

Comentários podem ter diferentes metadados (nome, email, data, respostas) que podem variar de um comentário para outro. O modelo de documentos armazena dados em formatos como JSON, permitindo essa flexibilidade, onde cada documento pode ter sua própria estrutura podendo adicionar novos campos (ex. moderado, oculto, editado) facilmente sem modificar uma tabela inteira ou impactar outras partes do sistema. Em um blog social, postagens podem ter milhares de comentários, e as consultas podem aumentar exponencialmente. O modelo de documentos permite armazenar todos os comentários de uma postagem juntos, em um documento único ou em coleções, melhorando o desempenho de leitura e escrita.


**Estrutura do Documento em JSON**:

- Coleção usuários: <br>
{ <br>
  "_id": "123", <br>
  "nome": "João Silva", <br>
  "email": "joao.silva@email.com", <br>
  "data_entrada": "2024-01-15", <br>
  "periodo": "setimo" <br>
} <br>

- Coleção posts: <br>
{ <br>
  "_id": "456", <br>
  "conteudo": "Esse é o conteúdo do post", <br>
  "id_usuario": "123", <br>
  "interacoes": 10, <br>
  "timestamp": "2024-09-15T14:30:00Z" <br>
} <br>

- Coleção comentários: <br>
{ <br>
  "_id": "789", <br>
  "id_post": "456", <br>
  "conteudo": "Esse é o primeiro comentário", <br>
  "timestamp": "2024-09-15T15:00:00Z", <br>
  "id_comentario_pai": null <br>
} <br>
{ <br>
  "_id": "790", <br>
  "id_post": "456", <br>
  "conteudo": "Esse é um comentário em resposta ao primeiro comentário", <br>
  "timestamp": "2024-09-15T16:00:00Z", <br>
  "id_comentario_pai": "789" <br>
} <br>


**Relação entre a coleção de documentos**:

![Diagrama Blog drawio](https://github.com/user-attachments/assets/98f3948b-4990-4c2f-8d86-b9c508c5ebc8)
