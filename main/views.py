from django.core.mail import BadHeaderError, send_mail
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.http import HttpResponse
from django.db import connection

from . import serializers

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Event, Category, PopularCourse, Review, LessonInfo
from .serializers import EventSerializer, CategorySerializer, PopularCourseSerializer, ReviewSerializer, \
    LessonInfoSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language_code'] = self.request.query_params.get('language',
                                                                 'en')
        return context

    @action(detail=False, methods=['post'])
    def update_order(self, request):
        order_data = request.data.get('order', [])
        for index, item_id in enumerate(order_data):
            Category.objects.filter(id=item_id).update(order=index)
        return Response({'status': 'order updated'})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Category

@csrf_exempt
@require_POST
def update_category_order(request):
    import json
    data = json.loads(request.body)
    order = data.get('order', [])

    for index, category_id in enumerate(order):
        try:
            category = Category.objects.get(id=category_id)
            category.order = index
            category.save()
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Invalid category id'}, status=400)

    return JsonResponse({'status': 'order updated'})


class PopularCourseViewSet(viewsets.ModelViewSet):
    queryset = PopularCourse.objects.all()
    serializer_class = PopularCourseSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language_code'] = self.request.query_params.get('language',
                                                                 'en')
        return context


class LessonInfoViewSet(viewsets.ModelViewSet):
    queryset = LessonInfo.objects.all()
    serializer_class = LessonInfoSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language_code'] = self.request.query_params.get('language',
                                                                 'en')
        return context


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language_code'] = self.request.query_params.get('language',
                                                                 'en')
        return context


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language_code'] = self.request.query_params.get('language',
                                                                 'en')
        return context


def reset_database(request):
    with connection.cursor() as cursor:
        cursor.execute("DROP SCHEMA public CASCADE;")
        cursor.execute("CREATE SCHEMA public;")
    return HttpResponse("Database reset successfully.")


class ContactFormView(APIView):
    serializer_class = serializers.ContactFormSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']
            print(name, email, message)
            if name and message and email:
                try:
                    send_mail(
                        'Subject here',
                        f'Name: {name}\nEmail: {email}\nMessage: {message}',
                        'beglaryan4.arman@gmail.com',
                        ['gekoeducation@gmail.com'],
                        fail_silently=False
                    )
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")
                return Response({'message': 'Email sent successfully'}, status=200)
            else:
                return HttpResponse("Make sure all fields are entered and valid.")
        else:
            return Response(serializer.errors, status=400)
