# Generated by Django 3.2.16 on 2022-12-25 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Departman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='واحد')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50, verbose_name='عنوان')),
                ('text', models.TextField(verbose_name='متن تیکت')),
                ('answer', models.TextField(verbose_name='پاسخ')),
                ('answerd', models.BooleanField(default=False, verbose_name='وضعیت پاسخ')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')),
                ('departman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.departman', verbose_name='واحد')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
    ]
