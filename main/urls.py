from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'popular_courses',
                views.PopularCourseViewSet, basename='popularcourse')
router.register(r'lesson_info', views.LessonInfoViewSet, basename='lessoninfo')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'events', views.EventViewSet, basename='event')
urlpatterns = [
    path('', include(router.urls)),
    path('reset-database/', views.reset_database, name='reset_database'),
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
]
