# Generated by Django 4.2.9 on 2024-04-30 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0016_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='feedback_content',
            field=models.TextField(blank=True, max_length=300),
        ),
    ]
