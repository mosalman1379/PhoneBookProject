from django.urls import path
from phones.views import find_entry, CreateEntry, Login, Logout, ShowContact, EditContact

app_name = 'phones'
urlpatterns = [
    path('find/', find_entry, name='find'),
    path('search/', ShowContact.as_view(), name='search'),
    path('register/', CreateEntry.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('', Login.as_view(), name='login'),
    path('edit/<int:pk>/', EditContact.as_view(), name='edit')
]
