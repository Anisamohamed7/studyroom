# Generated by Django 5.1.2 on 2024-12-06 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyroom', '0005_room_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
