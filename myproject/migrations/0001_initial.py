# Generated by Django 3.2.15 on 2022-10-06 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=200)),
                ('reporter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myproject.reporter')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('headline', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('pub_date', models.DateField()),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myproject.reporter')),
                ('tags', models.ManyToManyField(to='myproject.Tag')),
            ],
        ),
    ]