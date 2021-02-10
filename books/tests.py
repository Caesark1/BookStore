from django.test import TestCase
from .models import Book, Review
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class BookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="reviewUser",
            email = 'rtest@gmail.com',
            password = 'testpassword'
        )
        self.special_permission = Permission.objects.get(codename = 'special_status')
        self.book = Book.objects.create(title="Test Book", author="Test Author", price="39.00")
        self.review = Review.objects.create(book = self.book, review="Sometest here for reviews", author = self.user)
    
    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Test Book')
        self.assertEqual(f'{self.book.author}', 'Test Author')
        self.assertEqual(f'{self.book.price}', '39.00')

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(email = 'rtest@gmail.com', password = 'testpassword')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertTemplateUsed(response, 'books/book_list.html')
    
    def test_book_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/books/' % (reverse('account_login')))
        response = self.client.get('%s?next=/books/' % (reverse('account_login')))
        self.assertContains(response, 'Log In')
    
    def test_book_detail_view_with_permissions(self):
        self.client.login(email='rtest@gmail.com', password='testpassword')
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Book')
        self.assertContains(response, 'Sometest here for reviews')
        self.assertTemplateUsed(response, 'books/book_detail.html')
