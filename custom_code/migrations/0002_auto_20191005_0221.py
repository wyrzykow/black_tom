# Generated by Django 2.2.6 on 2019-10-05 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_code', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tnstarget',
            options={'get_latest_by': ('-name',), 'ordering': ('-id',)},
        ),
    ]