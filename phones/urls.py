from django.urls import path

from phones.views import create_entry, find_entry, show_search_form, show_add_entry_form

app_name = 'phones'
urlpatterns = [
    path('create/', create_entry, name='create'),
    path('find/', find_entry, name='find'),
    path('search/', show_search_form, name='search'),
    path('', show_add_entry_form, name='show_add_entry_form')
]
