# Generated by Django 4.2.8 on 2023-12-19 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ChlorineWater', '0002_rename_uid_chlorinedata_loginid'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('Name', models.CharField(db_column='Name', max_length=50)),
                ('loginid', models.CharField(db_column='loginid', max_length=50)),
                ('roleid', models.IntegerField(default=1)),
                ('orgid', models.IntegerField(blank=True, default=1, null=True)),
                ('region', models.IntegerField(blank=True, default=1, null=True)),
                ('portion', models.IntegerField(blank=True, default=1, null=True)),
                ('user_group', models.IntegerField(blank=True, default=1, null=True)),
                ('stock_alltr', models.IntegerField(blank=True, default=1, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]