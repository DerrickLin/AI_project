# Generated by Django 5.0.1 on 2024-02-03 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0003_alter_register_options_alter_register_managers_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="register",
            name="email",
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name="register",
            name="password",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="register",
            name="username",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
