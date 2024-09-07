from django.core.mail import BadHeaderError, send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.db import connection
from . import serializers

import requests
import json
import os


def reset_database(request):
    with connection.cursor() as cursor:
        cursor.execute("DROP SCHEMA public CASCADE;")
        cursor.execute("CREATE SCHEMA public;")
    return HttpResponse("Database reset successfully.")


# def translations_view(request, lang_code):
#     translations = {
#         'part1': _('English part1') if lang_code == 'en' else _('Other language part1'),
#         'HOME': _('Home') if lang_code == 'en' else _('Other language Home'),
#         'ABOUT_US': _('About us') if lang_code == 'en' else _('Other language About us'),
#         'BLOG': _('Blog') if lang_code == 'en' else _('Other language Blog'),
#         'CONTACTS': _('Contacts') if lang_code == 'en' else _('Other language Contacts'),
#         'COURSES': _('Courses') if lang_code == 'en' else _('Other language Courses'),
#         'EVENTS': _('Events') if lang_code == 'en' else _('Other language Events'),
#         'TERMINATES': _('Terminates'),  # Если термин один и тот же для всех языков
#     }
#     return JsonResponse(translations)

def translate_and_save(text, target_language):
    # Используем Google Translate для получения перевода
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        'q': text,
        'target': target_language,
        'key': settings.GOOGLE_TRANSLATE_API_KEY
    }
    response = requests.post(url, params=params)

    if response.status_code == 200:
        translated_text = response.json()['data']['translations'][0]['translatedText']
        save_translation_to_po_file(text, translated_text, target_language)
    else:
        raise Exception("Ошибка при переводе текста")

def save_translation_to_po_file(original_text, translated_text, language_code):
    locale_dir = os.path.join(settings.BASE_DIR, 'locale', language_code, 'LC_MESSAGES')
    po_file_path = os.path.join(locale_dir, 'django.po')

    # Создаем файл если его нет
    if not os.path.exists(locale_dir):
        os.makedirs(locale_dir)

    with open(po_file_path, 'a') as po_file:
        po_file.write(f'\nmsgid "{original_text}"\nmsgstr "{translated_text}"\n')


def load_translations(lang_code):
    file_path = os.path.join(settings.BASE_DIR, 'translations', f'{lang_code}.json')
    if not os.path.exists(file_path):
        return {}

    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def translations_view(request, lang_code):
    translations = load_translations(lang_code)
    return JsonResponse(translations)
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
