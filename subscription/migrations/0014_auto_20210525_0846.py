# Generated by Django 2.2 on 2021-05-25 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("subscription", "0013_auto_20210524_0558")]

    operations = [
        migrations.AlterModelOptions(
            name="subscription",
            options={
                "verbose_name": "Subscription",
                "verbose_name_plural": "Subscriptions",
            },
        ),
        migrations.RenameField(
            model_name="subscription", old_name="currency", new_name="product_currency"
        ),
        migrations.RenameField(
            model_name="subscription",
            old_name="description",
            new_name="product_description",
        ),
        migrations.RenameField(
            model_name="subscription", old_name="name", new_name="product_name"
        ),
        migrations.RenameField(
            model_name="subscription", old_name="price", new_name="product_price"
        ),
    ]
