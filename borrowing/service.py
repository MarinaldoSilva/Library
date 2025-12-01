from datetime import date, timedelta
from django.db import transaction
from rest_framework.exceptions import ValidationError
from borrowing.models import Borrowing

def service_create(user, book, return_date):

    if not user.status or book is None:
        raise ValidationError("Usuário inativo no sistema ou Livro não enviado.")

    if book.status != "AVAILABLE":
        raise ValidationError("Livro reservado ou não disponível.")

    if return_date is None or return_date <= date.today():
        raise ValidationError("A data de devolução deve ser posterior à data atual.")
    
    limit_borrowing = Borrowing.objects.filter(
        user=user, 
        return_date__gte=date.today()
    ).count()
    
    if limit_borrowing >= 5:
        raise ValidationError("O limite de empréstimos de livros é 5.")

    if book.category == "Raro" and not user.is_staff:
        raise ValidationError("Livros 'Raros' não podem ser emprestados por usuários comuns.")
            
    usuario_tem_livro_da_categoria = Borrowing.objects.filter(
        user=user, 
        book__category__iexact=book.category,
        return_date__gte=date.today()
    ).exists()
    
    if usuario_tem_livro_da_categoria:
        raise ValidationError(
            f"Já existe um livro da categoria '{book.category}' na sua biblioteca. Somente um por categória é liberado no sistema.")

    data_limite_lancamento = book.publication_date + timedelta(days=30)
    livro_em_lancamento = date.today() <= data_limite_lancamento

    if livro_em_lancamento:
        verifica_emprestimos_pendentes = Borrowing.objects.filter(
            user=user, 
            return_date__lt=date.today()
        ).exists()
        
        if verifica_emprestimos_pendentes:
            raise ValidationError("Usuário com pendências não pode pegar lançamentos.")

    with transaction.atomic():
        borrowing = Borrowing.objects.create(
            user=user,
            book=book,
            return_date=return_date
        )

        book.status = 'BORROWED'
        book.save()

    return borrowing