# Generated by Django 4.0.1 on 2023-05-09 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staticcharges', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticcharge',
            name='identifier',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]