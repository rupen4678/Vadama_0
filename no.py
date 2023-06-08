from django.db import migrations, models

def set_default_username(apps, schema_editor):
    add_product = apps.get_model('home', 'add_product')
    add_product.objects.filter(username__isnull=True).update(username_id=1)

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_product',
            name='username',
            field=models.ForeignKey(on_delete=models.CASCADE, to='auth.User'),
        ),
        migrations.RunPython(set_default_username),
    ]
