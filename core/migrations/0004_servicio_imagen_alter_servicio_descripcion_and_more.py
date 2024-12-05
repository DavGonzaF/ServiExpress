# Generated by Django 5.1.4 on 2024-12-04 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_servicio_boleta_carrito_itemcarrito_itemboleta'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='servicios/'),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='nombre',
            field=models.CharField(max_length=255),
        ),
    ]