# BD-NoSql
Rede social para GI?

Authors: Letícia Machado e George Lucas

Descreva as informações dos usuários.


O Sistema de Comentários para um Blog irá permitir que os usuários publiquem comentários em postagens específicas. Os comentários devem ser associados a uma postagem, conter o nome do autor, o texto do comentário, data/hora da criação, e podem permitir respostas entre os comentários, criando conversas encadeadas. O sistema deverá ser eficiente na leitura de grandes volumes de dados (vários comentários por postagem) e flexível para gerenciar metadados de comentários e respostas.
A escolha de um banco de dados NoSQL baseado em modelo de documentos, é ideal para essa aplicação devido à flexibilidade e simplicidade no armazenamento de dados sem a necessidade de estruturas rígidas como tabelas e relações fixas.
Comentários podem ter diferentes metadados (nome, email, data, respostas) que podem variar de um comentário para outro. O modelo de documentos armazena dados em formatos como JSON, permitindo essa flexibilidade, onde cada documento pode ter sua própria estrutura podendo adicionar novos campos (ex. moderado, oculto, editado) facilmente sem modificar uma tabela inteira ou impactar outras partes do sistema.
Em um blog, postagens podem ter milhares de comentários, e as consultas podem aumentar exponencialmente. O modelo de documentos permite armazenar todos os comentários de uma postagem juntos, em um documento único ou em coleções, melhorando o desempenho de leitura e escrita.

Firebase

Exemplo da Estrutura do Documento em JSON :
{
  "post_id": "12345",
  "comments": [
    {
      "comment_id": "1",
      "author": "User1",
      "content": "Ótimo artigo!",
      "timestamp": "2024-09-16T10:00:00Z",
      "replies": [
        {
          "comment_id": "2",
          "author": "User2",
          "content": "Concordo!",
          "timestamp": "2024-09-16T10:05:00Z"
        }
      ]
    },
    {
      "comment_id": "3",
      "author": "User3",
      "content": "Achei interessante essa parte...",
      "timestamp": "2024-09-16T10:10:00Z"
    }
  ]
}


Relação entre a coleção de documentos:


![Diagrama Blog drawio](https://github.com/user-attachments/assets/f1210768-f708-4f91-9bf2-15e8d947b84d)
