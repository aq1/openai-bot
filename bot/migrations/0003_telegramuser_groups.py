# Generated by Django 4.2 on 2023-05-03 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('bot', '0002_rename_user_telegramuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='groups',
            field=models.ManyToManyField(related_name='telegram_users', to='auth.group'),
        ),
    ]
