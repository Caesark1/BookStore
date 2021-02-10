from django.shortcuts import render
from .models import Book
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    login_url = 'account_login'


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    login_url = 'account_login'   
    permission_required = 'books.special_status' 


class SearchResultListView(ListView):
    model = Book
    template_name = 'books/search_result.html'
    context_object_name = 'books'
    def get_queryset(self):
        query_title = self.request.GET.get('title')
        query_author = self.request.GET.get('author')
        print(len(self.request.GET))
        return Book.objects.filter(
            Q(title__icontains = query_title) | Q(author__icontains = query_author)
        )
