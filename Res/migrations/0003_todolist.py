# Generated by Django 4.0.5 on 2022-08-28 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Res', '0002_remove_user_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('body', models.CharField(max_length=500)),
            ],
        ),
    ]
