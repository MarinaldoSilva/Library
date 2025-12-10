# REVISÃO DE MARINALDO SILVA

## Descrição:
Essas correções tem o intuito de instruir o desenvolvedor que está começando a melhorar suas skills, aprender com `devs` mais experientes, além de direcionar para a cultura organizacional do time de tecnologia seguindo boas práticas de programação.

## Correções:

**A documentação da api precisa ser mais organizada**

Quando a documentação é gerada, os endpoints ficam colados e sem separação de app, é necessário usar a `Tags=['Book']` (Exemplo), e em cada endpoint relacionado a "Book" usar essa tag para gerar a doc do swagger. 

**Houve uma falha na criação de usuário em definir o campo `Email` como um index da model e colocar dentro do array de campo obrigatório da model**

```py
class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=False)
    birth_date = models.DateField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["birth_date", "full_name"]

    def __str__(self):
        return f"Usuário {self.username} criado com sucesso."
```

Poderia colocar 

```py
  REQUIRED_FIELDS = ["email","birth_date", "full_name"]
```
**Erro no método `__str__`**

Tem uma falha tambem no método `__str__` da model, foi colocado uma mensagem de retorno como se fosse uma "Response" de uma view, mas na verdade a função `str` cria uma representação da tabela no banco de dados e não uma mensagem de resposta

```py

    def __str__(self):
        return f"Usuário {self.username} criado com sucesso."
```

poderia ser 

```py

  def __str__(self):
        return f"{self.username} - {self.email}"
```
**Falta de instruções de teste** 
É importante deixar claro para o avaliador como executar os testes, então sempre deixe instruções claras de teste

**Erro de N+1**

Esse erro acontece quando uma consulta no banco é feita varias vezes no mesmo endpoint, exemplo eu quero buscar todos os livros do banco e nessa `query` eu busco os livros e faz +1 query buscando os autores, e nisso vai seguido para cada livro.

- código para ajuste

```py
class BookListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Listar Livros", description="Lista os livros. Admins veem todos; usuários também podem ver todos ou aplicar filtros no cliente.", responses={200: BookSerializer(many=True)})
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

Muitos if's e poderia usar o `selected_related()` para resolver esse problema de N+1

**Remover campos não pedidos como `estoque` que até destoam do que foi pedido, campos em inglês** 
Sempre que possível, siga estritamente as instruções solicitadas, se case queiram mudar algo, gere um ADR para avaliação. 

### Empréstimos

- **Modelagem de `Borrowing` muito minimalista**
  - Campos: `id` (UUID), `user`, `book`, `borrow_date`, `return_date`.
  - Não existe campo de `status` do empréstimo.
  - Efeitos:
    - não há rastreio de histórico de devolução/atraso;
    - fica mais difícil evoluir para regras de multa ou relatório.
  - Para um Júnior 1, é compreensível começar simples, mas é um ponto claro de evolução futura.

- **“Devolução” apaga o empréstimo**
  - `BorrowingDeleteAPIView`:
    - recupera o empréstimo;
    - define `book.status = "AVAILABLE"` e salva;
    - chama `queryset.delete()` no `Borrowing`.
  - Isso devolve o livro, mas **apaga o histórico** do empréstimo.
  - Em sistemas reais costuma-se:
    - manter o registro do empréstimo e mudar apenas o status (e/ou data de devolução efetiva).

- **Bug em `PATCH` de empréstimo (update parcial)**
  - `BorrowingUpdateAPIView` usa `BorrowingSerializer(..., partial=True)`.
  - No `BorrowingSerializer.validate`:
    - se `book` não vier em `data`, é levantado `"Livro é obrigatório."`.
  - Em um patch normal (ex.: mudar só `return_date`), o cliente não deveria precisar reenviar o livro.
  - Resultado: na prática, o update parcial tende a falhar se o `book` não for reenviado.
  - Ajuste esperado:
    - em updates, usar `book = data.get("book") or self.instance.book` (quando `self.instance` existe).

- **Concorrência e consistência do status do livro**
  - Disponibilidade é checada no serializer:
    - `if book.status != "AVAILABLE": raise ValidationError(...)`.
  - O status só é alterado para `"BORROWED"` **depois**, na view `BorrowingCreateAPIView`.
  - Entre a validação e o salvamento, duas requisições concorrentes podem passar, gerando dois empréstimos do mesmo livro.
  - É um ponto mais avançado, mas vale citar como evolução:
    - uso de `transaction.atomic()`;
    - revalidação no nível do model;
    - ou `select_for_update()` em consultas críticas.

- **Renovação simplificada**
  - `BorrowingRenewalAPIView`:
    - impede renovação se `book.status == "RESERVED"`;
    - soma 7 dias ao `return_date`.
  - Não verifica:
    - se o empréstimo já está vencido;
    - limite de renovações;
    - nenhum status de empréstimo.
  - Não é um bug, mas é uma modelagem mais simples do que as usadas em sistemas de biblioteca.