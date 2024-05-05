from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from . import models


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
                        ['bukboks1@gmail.com'],
                        fail_silently=False
                    )
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")
                return Response({'message': 'Email sent successfully'}, status=200)
            else:
                return HttpResponse("Make sure all fields are entered and valid.")
        else:
            return Response(serializer.errors, status=400)


class LessonListCreate(generics.ListCreateAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = serializers.LessonSerializer


class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = serializers.LessonSerializer


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
