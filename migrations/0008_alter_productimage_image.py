# Generated by Django 4.0.1 on 2023-05-05 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_add_product_image_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.FileField(upload_to='image/'),
        ),
    ]
