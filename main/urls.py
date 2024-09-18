from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, EventViewSet, CategoryViewSet, PopularCourseViewSet, \
    LessonInfoViewSet, update_category_order

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'popular_courses',
                PopularCourseViewSet, basename='popularcourse')
router.register(r'lesson_info', LessonInfoViewSet, basename='lessoninfo')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'events', EventViewSet, basename='event')
urlpatterns = [
    path('', include(router.urls)),
    path('update-order/', update_category_order, name='update-order'),
    path('reset-database/',
         views.reset_database, name='reset_database'),
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
]
