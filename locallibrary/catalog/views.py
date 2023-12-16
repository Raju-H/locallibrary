from django.shortcuts import render
from catalog.models import *

# Create your views here.

def index(request):
    number_of_books = Book.objects.all().count()
    number_of_instances = BookInstance.objects.all().count()
    number_of_instances_available = BookInstance.objects.filter(status__exact='a').count()
    number_of_authors = Author.objects.all().count()

    context = {
        'number_of_books': number_of_books,
        'number_of_instances': number_of_instances,
        'number_of_instances_available': number_of_instances_available,
        'number_of_authors': number_of_authors,
    }
    return render(request, 'index.html', context=context)
