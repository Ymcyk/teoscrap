# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 11:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ArticleWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('words_number', models.PositiveIntegerField(default=1)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='articleword',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Word'),
        ),
        migrations.AddField(
            model_name='article',
            name='article_words',
            field=models.ManyToManyField(through='blog.ArticleWord', to='blog.Word'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Author'),
        ),
    ]
