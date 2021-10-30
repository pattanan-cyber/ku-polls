# Generated by Django 3.2.6 on 2021-10-30 05:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0002_end_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
        migrations.AddField(
            model_name='votes',
            name='choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.choice'),
        ),
        migrations.AddField(
            model_name='votes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
