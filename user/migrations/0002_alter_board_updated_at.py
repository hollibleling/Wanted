# Generated by Django 3.2.8 on 2021-10-22 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]