# Generated by Django 2.2.16 on 2023-04-24 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20230424_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='posts/', verbose_name='Картинка'),
        ),
    ]
