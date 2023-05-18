# Generated by Django 4.2.1 on 2023-05-18 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_user_imageurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='imageurl',
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(null=True, upload_to='profile_images/'),
        ),
    ]