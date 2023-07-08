# Generated by Django 4.1.3 on 2022-11-26 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaticCharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_amount', models.CharField(max_length=50)),
                ('max_amount', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=225)),
                ('ext_static_charge_id', models.CharField(max_length=50)),
                ('lnurlp', models.CharField(max_length=250)),
            ],
        ),
    ]