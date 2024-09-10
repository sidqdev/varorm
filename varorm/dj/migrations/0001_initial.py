# Generated by Django 4.1.5 on 2024-09-10 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DBStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('hkey', models.CharField(max_length=255)),
                ('value', models.TextField(null=True)),
            ],
            options={
                'db_table': 'varorm_db_storage',
                'unique_together': {('key', 'hkey')},
            },
        ),
    ]
