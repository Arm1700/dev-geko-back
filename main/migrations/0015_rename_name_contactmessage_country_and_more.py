# Generated by Django 5.0.4 on 2024-11-12 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_remove_lessoninfo_count_remove_lessoninfo_icon_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactmessage',
            old_name='name',
            new_name='country',
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.category'),
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='full_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='whatsapp',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
