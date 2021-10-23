# Generated by Django 3.2.8 on 2021-10-23 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('initz', '0002_auto_20211023_0705'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(default='No Document Title Set', max_length=200)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('initiative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='initz.initiative')),
            ],
        ),
    ]
