# API de Gerenciamento de Biblioteca

## Projeto

Projeto desenvolvido de forma autônoma, usando como base a documentação do Django Rest Framework e muita pesquisa.
O projeto em si consiste em uma API de Gerenciamento de Biblioteca, para desenvolvimento usei os princípios S.O.L.I.D. mas tomei cuidado para não ser verboso,
a simplicidade foi meu foco para ser funcional, esse foi o objetivo. Com esse sistema é possível que um usuário se cadastre com a única rota liberada para acesso sem precisar de validação
de usuário/senha e Token, após isso o user tem duas opções:

1. Visualizar os dados de livros e autores.
2. Realizar empréstimos de livros que estejam disponíveis.

Para que isso seja possível foram criadas funções e validações de acordo com as regras de negócio.

## Processo de criação

Esse foi o projeto com uma lógica simples ao mesmo tempo complexa que tem como o core central a validação de regras de negócio dentro do Serializer e a consistência de dados nas Views.
Optei pelo controle e flexibilidade usando APIView. O usuário é injetado pela view quando a requisição é feito na request, quando um usuário autenticado faz a requisição,
o processo de verificar se o usuário está ativo, contar quantos empréstimos ativos o usuário possui,
validar se a data de devolução é valida a hoje, verificar status do livro para saber se está reservado ou emprestado.
Isso é feito feito quando o `serializer.is_valid()` é chamado. Após isso, na camada da View, temos a manipulação do banco de dados: ao criar o empréstimo,
o status do livro é automaticamente alterado de AVAILABLE para BORROWED. Caso aconteça algo nesse processo, uma mensagem do erro com o status vai ser fornecido para o cliente,
assim facilitando a identificação do erro.

O projeto conta com tecnologias como:

- Autenticação por tokens do JWT
- Documentação automática com Swagger (drf-spectacular)

## Funções

### Empréstimos

- Validação de limite de 5 livros por usuário
- Não permitir um empréstimo se o livro estiver com status diferente de 'AVAILABLE'
- Atualização automática do status do livro na retirada e na devolução
- Endpoint específico para renovação de empréstimo

### Livros e Autores

- CRUD para livros e autores
- Serializador aninhado para exibir dados do autor junto com o livro

### Usuários

- Cadastro de novos usuários
- Login com uso de Token JWT
- Permissões especiais para Administradores

## Endpoints

Sendo extremamente honesto, não foi fácil fazer isso, envolveu muito estudo e dedicação, agora eu vejo como ficou e penso "na teoria é simples, na prática a gente sofre",
mas a vida é assim, com o passar do tempo vamos fazer isso de forma natural. Vamos listar os principais endpoints da API.

### Criar user (Sign Up)

Na rota:

```http
http://127.0.0.1:8000/api/v1/auth/register/
```

Informamos nossas credenciais do cadastro

```json
{
  "username": "mario",
  "email": "mario@hotmail.com",
  "password": "admin@2025",
  "first_name": "mario",
  "last_name": "joaqui",
  "full_name": "mario joaquim",
  "birth_date": "1995-10-25",
  "status": true
}
```

e nossa view lida com isso.

### Login (Gerar Token)

Com as credenciais já em mãos, vamos gerar os tokens de acesso.
Na rota:

```http
http://127.0.0.1:8000/api/v1/auth/login/
```

```json
{
  "email": "mario@hotmail.com",
  "password": "admin@2025"
}
```

é retornado os nossos tokens de acesso.

```json
{
  "id": 1,
  "username": "mario",
  "email": "mario@hotmail.com",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0MDc1MjIyLCJpYXQiOjE3NjM5ODg4MjIsImp0aSI6IjQyZDFlZjdlMGYwYjQ1OTI5OTQxZjc5OGQ2OTdiZGNlIiwidXNlcl9pZCI6IjEifQ.tQ5kLvJcNFuXL50GOiqcSuX6sXFzNTEgaNmYBodV4x8",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NDY4MDAyMiwiaWF0IjoxNzYzOTg4ODIyLCJqdGkiOiI1Y2I5ZjYzMDgzYjQ0MzhkYjBmODllOWVmMzkyMjc4MiIsInVzZXJfaWQiOiIxIn0.HeeuW40tclww-gtWP9JnzCQ2P_VA67AT376V0TcsuSQ"
}
```

e com esses tokens vamos ter acesso a nossa aplicação RestFull por completo.

### Logout (Sair do sistema)

para sair do sistema vamos precisar dos tokens de acess e refresh.

Na rota:

```http
http://127.0.0.1:8000/api/v1/auth/logout/
```

vamos passar nosso refresh no body e nosso token access no auth.

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NDMzNDU0NSwiaWF0IjoxNzYzNjQzMzQ1LCJqdGkiOiIwM2Y3YTUxYWNkNzk0Mzg1ODU3NzEwM2I2YTE3NzBjMyIsInVzZXJfaWQiOiIxIn0.ZTRPzt4e8JmM4weh5h0jm-6Bnn44hzpo_16JCSNuvxY"
}
```

O nosso retorno é um `204 no content`:
No body returned for response

### Cadastrar Autores(Author)

Na rota:

```json
 http://127.0.0.1:8000/api/v1/authors/
```

vamos cadastrar os autores dos livros.

```json
{
  "name": "Felipe Luiz",
  "biography": "{% faker 'randomJobDescriptor' %}",
  "birth_date": "1949-05-26",
  "nationality": "BR"
}
```

e o nosso retorno será com esse formato, porém precismos anotar o id.

```json
{
  "id": "0bcb6104-9159-4201-a712-4953fb0e66ec",
  "name": "Felipe Luiz",
  "biography": "Forward",
  "birth_date": "1949-05-26",
  "nationality": "BR"
}
```

Agora que temos um usuário e um autor, podemos vincular um autor ao livro.

### Cadastrar Livros

Para cadastrar um livro ou muitos livros de uma vez.

Na rota:

Na rota:

```http
http://127.0.0.1:8000//api/v1/library/books/create/
```

com os dados:

```json
{
  "title": "Clean Code",
  "subtitle": "A Handbook of Agile Software Craftsmanship",
  "book_description": "Even bad code can function. But if code isn't clean, it can bring a development organization to its knees.",
  "category": "Tecnologia",
  "publisher": "Prentice Hall",
  "last_edition": "2008-08-01",
  "ISBN": "978-0132350884",
  "page_count": 464,
  "language": "Inglês",
  "cover_url": "https://example.com/cleancode.jpg",
  "status": "AVAILABLE",
  "estoque": 15,
  "author": null
}
```

cadastramos um livro, para cadastrar vários livro com uma única requisição:

```json
[
  {
    "title": "Clean Code",
    "subtitle": "A Handbook of Agile Software Craftsmanship",
    "book_description": "Even bad code can function. But if code isn't clean, it can bring a development organization to its knees.",
    "category": "Tecnologia",
    "publisher": "Prentice Hall",
    "last_edition": "2008-08-01",
    "ISBN": "978-0132350884",
    "page_count": 464,
    "language": "Inglês",
    "cover_url": "https://example.com/cleancode.jpg",
    "status": "AVAILABLE",
    "estoque": 15,
    "author": null
  },
  {
    "title": "O Senhor dos Anéis: A Sociedade do Anel",
    "subtitle": "Volume 1",
    "book_description": "O início da grande jornada de Frodo Bolseiro para destruir o Um Anel.",
    "category": "Fantasia",
    "publisher": "HarperCollins",
    "last_edition": "2019-11-25",
    "ISBN": "978-8595084742",
    "page_count": 576,
    "language": "Português",
    "cover_url": null,
    "status": "AVAILABLE",
    "estoque": 8,
    "author": null
  }
]
```

Assim podemos cadastrar mais de um livro por vez.

### Vincular autores

Na rota:

```json
http://127.0.0.1:8000/api/v1/library/books/create/
```

vamos criar e vincular um author a um livro.

```json
{
  "title": "A Revolução dos Bichos",
  "subtitle": "A distopia dos animais",
  "book_description": "{% faker 'randomJobDescriptor' %}",
  "author": "c217dfd2-91a6-4e4f-8e77-501581f75af9",
  "category": "Politica",
  "publisher": "Editora Clássica",
  "last_edition": "2025-05-15",
  "ISBN": "{% faker 'randomMACAddress' %}",
  "page_count": 320,
  "language": "Português",
  "cover_url": "{% faker 'randomImageUrl' %}",
  "status": "AVAILABLE",
  "estoque": 21
}
```

copiamos o ID no author e adicionamos no campo `author` que é uma chave estrangeira para a tabela Author e nossa reposta é aninhada.

```json
{
  "id": "9d1302f3-bb37-4cb4-89dc-027e1dded76e",
  "author_data": {
    "id": "c217dfd2-91a6-4e4f-8e77-501581f75af9",
    "name": "Brasileiro",
    "biography": "Chief",
    "birth_date": "1949-05-26",
    "nationality": "Inglês"
  },
  "title": "A Revolução dos Bichos",
  "subtitle": "A distopia dos animais",
  "book_description": "International",
  "category": "Politica",
  "publisher": "Editora Clássica",
  "publication_date": "2025-11-24",
  "created_at": "2025-11-24",
  "updated_at": "2025-11-24",
  "last_edition": "2025-05-15",
  "ISBN": "b6:26:e7:6a:d7:40",
  "page_count": 320,
  "language": "Português",
  "cover_url": "https://loremflickr.com/2715/2157?lock=3377547908260201",
  "status": "AVAILABLE",
  "estoque": 21,
  "author": "c217dfd2-91a6-4e4f-8e77-501581f75af9"
}
```

Nesse processo já atualizamos o Status do livro para marca-lo como reservado.

### Listar os livros cadastrados

Na rota:

```http
http://127.0.0.1:8000//api/v1/library/books/
```

```json
[
  {
    "id": "9d1302f3-bb37-4cb4-89dc-027e1dded76e",
    "author_data": {
      "id": "c217dfd2-91a6-4e4f-8e77-501581f75af9",
      "name": "Brasileiro",
      "biography": "Chief",
      "birth_date": "1949-05-26",
      "nationality": "Inglês"
    },
    "title": "A Revolução dos Bichos",
    "subtitle": "A distopia dos animais",
    "book_description": "International",
    "category": "Politica",
    "publisher": "Editora Clássica",
    "publication_date": "2025-11-24",
    "created_at": "2025-11-24",
    "updated_at": "2025-11-24",
    "last_edition": "2025-05-15",
    "ISBN": "b6:26:e7:6a:d7:40",
    "page_count": 320,
    "language": "Português",
    "cover_url": "https://loremflickr.com/2715/2157?lock=3377547908260201",
    "status": "AVAILABLE",
    "estoque": 21,
    "author": "c217dfd2-91a6-4e4f-8e77-501581f75af9"
  }
]
```

### Realizar empréstimo.

Na rota:

```http
http://127.0.0.1:8000/api/v1/borrowing/create/
```

Copiamos o ID do livro

```json
{
  "book": "9d1302f3-bb37-4cb4-89dc-027e1dded76e",
  "return_date": "2025-12-30"
}
```

Nessa view listamos um emprestimo pelo UUID/PK, e com isso fizemos nosso primeiro emprestimo.

### Listar empréstimos

Na rota vamos listar por UUID e geral:

```json
http://127.0.0.1:8000/api/v1/library/books/9d1302f3-bb37-4cb4-89dc-027e1dded76e
```

temos a nosso retorno.

```json
{
  "id": "9d1302f3-bb37-4cb4-89dc-027e1dded76e",
  "author_data": {
    "id": "c217dfd2-91a6-4e4f-8e77-501581f75af9",
    "name": "Brasileiro",
    "biography": "Chief",
    "birth_date": "1949-05-26",
    "nationality": "Inglês"
  },
  "title": "A Revolução dos Bichos",
  "subtitle": "A distopia dos animais",
  "book_description": "International",
  "category": "Politica",
  "publisher": "Editora Clássica",
  "publication_date": "2025-11-24",
  "created_at": "2025-11-24",
  "updated_at": "2025-11-24",
  "last_edition": "2025-05-15",
  "ISBN": "b6:26:e7:6a:d7:40",
  "page_count": 320,
  "language": "Português",
  "cover_url": "https://loremflickr.com/2715/2157?lock=3377547908260201",
  "status": "AVAILABLE",
  "estoque": 21,
  "author": "c217dfd2-91a6-4e4f-8e77-501581f75af9"
}
```

ou podemos apagar o ID/UUID na url e teremos esse retorno.

```json
{
  "id": "9d1302f3-bb37-4cb4-89dc-027e1dded76e",
  "author_data": {
    "id": "c217dfd2-91a6-4e4f-8e77-501581f75af9",
    "name": "Brasileiro",
    "biography": "Chief",
    "birth_date": "1949-05-26",
    "nationality": "Inglês"
  },
  "title": "A Revolução dos Bichos",
  "subtitle": "A distopia dos animais",
  "book_description": "International",
  "category": "Politica",
  "publisher": "Editora Clássica",
  "publication_date": "2025-11-24",
  "created_at": "2025-11-24",
  "updated_at": "2025-11-24",
  "last_edition": "2025-05-15",
  "ISBN": "b6:26:e7:6a:d7:40",
  "page_count": 320,
  "language": "Português",
  "cover_url": "https://loremflickr.com/2715/2157?lock=3377547908260201",
  "status": "AVAILABLE",
  "estoque": 21,
  "author": "c217dfd2-91a6-4e4f-8e77-501581f75af9"
}
```

### Renovação de empréstimos.

Na rota:

```http
http://127.0.0.1:8000/api/v1/borrowing/UUID/renew/
```

### Categoria e Ordenção

Por pesquisa na query pameters é possível ordenar por:

'category'
'auhtor'
'status'
'ordering'

e fazer o filtro por:

'titule'
'publication_date'
'author_name'

```py
def get(self, request):
        queryset = Book.objects.all()

        category = request.query_params.get('category')
        author_name = request.query_params.get('auhtor')
        status_param = request.query_params.get('status')
        ordering = request.query_params.get('ordering')

        if category:
            queryset = queryset.filter(category__icontains=category)

        if author_name:
            queryset = queryset.filter(author_name__icontains=author_name)

        if status_param:
            queryset = queryset.filter(status_param__icontains=status_param)

        search_validated = ['titule', 'publication_date', 'author_name']
        if ordering in search_validated:
            queryset = queryset.order_by(ordering)

        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

### Testes

Os teste é uma das partes mais complexas de serem feitas, até o momento os testes completos foram pelo client `Insomnia` e os testes no `pytest` foram somente
feitos para cobrir os processos básicos de criação de usuário e lógica de empréstimos.
Abaixo temos dois testes para criação de usuário e emprestimo, porém temos outras coberturas, e vamos desenvolvder mas coberturas para cobrir pelo menos 70% do sistema.

```py
class BorrowingTests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(username="mario", email="mario@gmail.com", password="admin@25", birth_date="2002-08-06", full_name="Mario Jb")
        self.client.force_authenticate(user=self.user)

        self.author = Author.objects.create(name="Sheldon Cupper", nationality="BR")

        self.book = Book.objects.create(title=" BIG BANG", ISBN="1234567890", page_count=100, author=self.author, status="AVAILABLE", last_edition="2023-01-01", estoque=1)

        self.url = reverse("borrowing-create")

    def test_borrwing_success(self):
        data = {"book": self.book.id, "return_date": date.today() + timedelta(days=7)}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, "BORROWED")
```

### Documentação

A documentação foi gerada com o Swegger, assim a visualização dos dados será mais amigável.

Na rota:

```http
http://127.0.0.1:8000/api/docs/
```

Ao acessar o link com o reposit´rio já baixado é possíevl ver toda a documentação do projeto.
