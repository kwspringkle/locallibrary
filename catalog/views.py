from urllib import request
from django.shortcuts import render
from django.views import generic, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Book, Author, BookInstance, Genre
from .constants import LOAN_STATUS, NUM_BOOK_VIEW, NUM_VISITS

# Create your views here.


def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=LOAN_STATUS.AVAILABLE.value
    ).count()
    num_authors = Author.objects.count()
    num_visits = request.session.get("num_visits", NUM_VISITS)
    request.session["num_visits"] = num_visits + NUM_VISITS

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instance_available": num_instances_available,
        "num_authors": num_authors,
        "num_visits": num_visits,
    }
    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = NUM_BOOK_VIEW
    context_object_name = "book_list"
    template_name = "catalog/book_list.html"
    queryset = Book.objects.all().order_by("title")


class BookDetailView(generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context["LOAN_STATUS"] = LOAN_STATUS
        context["book_instances"] = self.object.bookinstance_set.all()
        return context

    def book_detali_view(self, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, "catalog/book_detail.html", context={"book": book})


class LoanedBooksByUserListView(generic.ListView):
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = NUM_BOOK_VIEW

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact=LOAN_STATUS.ON_LOAN.value)
            .order_by("due_back")
        )
