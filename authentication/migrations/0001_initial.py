# Generated by Django 5.0.2 on 2024-03-17 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=500)),
                ('title', models.CharField(max_length=500)),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('description', models.TextField(max_length=5000)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('duration_minutes', models.IntegerField(blank=True, null=True)),
                ('duration_seconds', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]