# Generated by Django 4.1.5 on 2025-06-29 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=50)),
                ('customer_bio', models.CharField(blank=True, max_length=50, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_last_updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Customer',
                'db_table': 'CUSTOMER',
            },
        ),
    ]
