# Generated by Django 2.1.7 on 2021-01-30 06:42

import django.contrib.postgres.fields
from django.db import migrations, models
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0014_problem_share_submission'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleProblem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.TextField(db_index=True)),
                ('lang_type', models.TextField()),
                ('problem_type', models.TextField()),
                ('problem_title', models.TextField()),
                ('problem_content', utils.models.RichTextField()),
                ('options', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=120), size=None)),
                ('answers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=120), size=None)),
            ],
        ),
    ]
