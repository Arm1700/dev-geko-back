from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from . import serializers

@csrf_exempt
def my_view(request):
    return HttpResponse("ba urish")


class ContactFormView(APIView):
    def post(self, request):
        serializer = serializers.ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']

            send_mail(
                'Subject here',
                f'Name: {name}\nEmail: {email}\nMessage: {message}',
                'beglaryan4.arman@gmail.com',  # Замените на свой адрес отправителя
                ['bukboks1@gmail.com'],  # Замените на адрес получателя
                fail_silently=False,
            )
            return Response({'message': 'Email sent successfully'}, status=200)
        else:
            return Response(serializer.errors, status=400)
