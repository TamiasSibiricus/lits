# Generated by Django 3.2.16 on 2022-11-08 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0006_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'permissions': (('can_comment', 'Can leave comment for article'),)},
        ),
    ]
