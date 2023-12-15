from django.db import models
from uuid import uuid4
from django.urls import reverse

# Create your models here.
# common models
class CommonFields(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# genre model for locallibrary project and use uuid4 as a id
class Genre(CommonFields):
    name = models.CharField(max_length=200, help_text='Genre name', unique=True)

    def __str__(self):
        return self.name
    # return the url to access a particular genre instance
    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])

# book Model representing a book (but not a specific copy of a book)
class Book(CommonFields):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey("Language", verbose_name="Language", on_delete=models.CASCADE)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='<a href="(https://www.isbn-international.org/content/what-isbn)">13 Character ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        return self.title
    # return the url to access a particular book instance

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    # Create a string for the Genre. This is required to display genre in Admin.
    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'

# bookinstance Model representing a specific copy of a book (i.e. that can be borrowed from the library)

class BookInstance(CommonFields):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = [ 
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    ]
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
# Author Model representing a book author

class Author(CommonFields):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Date of death', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.full_name}'

# language model for locallibrary project
class Language(CommonFields):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
