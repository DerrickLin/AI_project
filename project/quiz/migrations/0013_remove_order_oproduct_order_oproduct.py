# Generated by Django 4.2.9 on 2024-03-24 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0012_alter_product_ploc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='oProduct',
        ),
        migrations.AddField(
            model_name='order',
            name='oProduct',
            field=models.ManyToManyField(to='quiz.product'),
        ),
    ]
