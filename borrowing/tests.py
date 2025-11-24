from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from author.models import Author
from book.models import Book
from borrowing.models import Borrowing

User = get_user_model()


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

    def test_book_not_avaliable(self):

        self.book.status = "BORROWED"
        self.book.save()

        data = {"book": self.book.id, "return_date": date.today() + timedelta(days=7)}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_borroeing_user_inactiv(self):

        self.user.status = False
        self.user.save()

        data = {"book": self.book.id, "return_date": date.today() + timedelta(days=7)}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_limite_de_5_livros(self):
        for i in range(5):
            livro_extra = Book.objects.create(title=f"Livro {i}", ISBN=f"111{i}", page_count=100, author=self.author, status="AVAILABLE", last_edition="2023-01-01", estoque=1)
            Borrowing.objects.create(user=self.user, book=livro_extra, return_date=date.today() + timedelta(days=5))

        data = {"book": self.book.id, "return_date": date.today() + timedelta(days=7)}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("5 livros" in str(response.data) or "5 books" in str(response.data))
