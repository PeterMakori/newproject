# Generated by Django 2.2.2 on 2019-06-25 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0015_notices_read_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notices',
            name='notice',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='sendfeedback',
            name='message',
            field=models.TextField(max_length=400),
        ),
        migrations.AlterField(
            model_name='sendfeedback',
            name='subject',
            field=models.CharField(max_length=200),
        ),
    ]