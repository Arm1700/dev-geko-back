from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='index'),
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
]
