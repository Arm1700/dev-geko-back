from django.urls import path
from . import views

urlpatterns = [
    path('reset-database/', views.reset_database, name='reset_database'),
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
    path('translations/<str:lang_code>/', views.translations_view, name='translations'),
]
