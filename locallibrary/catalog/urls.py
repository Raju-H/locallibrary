from django.urls import path
from catalog.views import *

urlpatterns = [
    path('', index, name='index'),
]
