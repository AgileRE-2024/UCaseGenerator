# Generated by Django 5.1.1 on 2024-11-16 10:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usecase', '0004_remove_usecase_aktor_remove_usecase_fitur_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_start', models.CharField(max_length=255)),
                ('feature_end', models.CharField(max_length=255)),
                ('use_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_connections', to='usecase.usecase')),
            ],
        ),
    ]