# Generated by Django 5.1.2 on 2024-12-06 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyroom', '0006_message_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='images/avatar.svg', null=True, upload_to=''),
        ),
    ]