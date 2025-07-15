from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from .constants import LOAN_STATUS
# Create your views here.


def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=LOAN_STATUS.AVAILABLE.value).count()
    num_authors = Author.objects.count()

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instance_available": num_instances_available,
        "num_authors": num_authors,
    }
    return render(request, "index.html", context=context)
