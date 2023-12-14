from django.db import models
from uuid import uuid4
from django.urls import reverse

# Create your models here.

# genre model for locallibrary project and use uuid4 as a id
class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, help_text='Unique ID for this particular genre')
    name = models.CharField(max_length=200, help_text='Genre name', unique=True)

    def __str__(self):
        return self.name
    # return the url to access a particular genre instance
    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])

# book Model representing a book (but not a specific copy of a book)
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey("Language", verbose_name="Language", on_delete=models.CASCADE) # fixed typo and verbose name
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character ISBN number (https://www.isbn-international.org/content/what-isbn)') # removed HTML link
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        return self.title
    # return the url to access a particular book instance

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

# bookinstance Model representing a specific copy of a book (i.e. that can be borrowed from the library)

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = [ # changed to list of tuples
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

class Author(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Date of death', null=True, blank=True) # changed verbose name

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.full_name}'

# language model for locallibrary project
class Language(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, help_text='Unique ID for this particular language')
    name = models.CharField(max_length=200) # removed redundant help text
    def __str__(self):
        return self.name
