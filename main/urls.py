from django.urls import path
from . import views

urlpatterns = [
    path('reset-database/', views.reset_database, name='reset_database'),
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
    path('categories/', views.CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroy.as_view(),
         name='category-retrieve-update-destroy'),
    path('lessons/', views.LessonListCreate.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', views.LessonRetrieveUpdateDestroy.as_view(), name='lesson-retrieve-update-destroy'),
]
