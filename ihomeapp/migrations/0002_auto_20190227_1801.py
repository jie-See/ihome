# Generated by Django 2.1.7 on 2019-02-27 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ihomeapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id_card',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='real_name',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
