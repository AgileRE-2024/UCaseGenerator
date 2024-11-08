# Generated by Django 5.1.1 on 2024-10-29 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usecase', '0002_actorfeature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aktor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Fitur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='usecase',
            old_name='title',
            new_name='nama',
        ),
        migrations.AddField(
            model_name='usecase',
            name='aktor',
            field=models.ManyToManyField(related_name='usecases', to='usecase.aktor'),
        ),
        migrations.AddField(
            model_name='usecase',
            name='fitur',
            field=models.ManyToManyField(related_name='usecases', to='usecase.fitur'),
        ),
    ]
