# Generated by Django 5.0.2 on 2024-03-24 10:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_remove_video_duration_minutes_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(blank=True, max_length=100, null=True)),
                ('lname', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.TextField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.TextField(blank=True, max_length=500, null=True)),
                ('url', models.URLField(blank=True, max_length=1000, null=True)),
                ('poster', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('time', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LiveStream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, max_length=500, null=True)),
                ('url', models.URLField(blank=True, max_length=1000, null=True)),
                ('poster', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('url', models.URLField(blank=True, max_length=1000, null=True)),
                ('poster', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('title1', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('article', models.TextField(blank=True, max_length=5000, null=True)),
                ('title2', models.CharField(blank=True, max_length=500, null=True)),
                ('image1', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('article2', models.TextField(blank=True, max_length=5000, null=True)),
                ('title3', models.CharField(blank=True, max_length=500, null=True)),
                ('image2', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('article3', models.TextField(blank=True, max_length=5000, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='video',
            name='user',
        ),
        migrations.AddField(
            model_name='video',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=5000)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='authentication.video')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ImageField(blank=True, null=True, upload_to='profile/')),
                ('bio', models.TextField(blank=True, default='', null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]