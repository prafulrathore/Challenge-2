# Generated by Django 2.2 on 2021-05-19 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0009_auto_20210519_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default='', max_length=100),
        ),
    ]