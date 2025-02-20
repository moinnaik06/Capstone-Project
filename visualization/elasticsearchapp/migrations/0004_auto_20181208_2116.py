from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elasticsearchapp', '0003_company_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.IntegerField(default=0)),
                ('compnumber', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('ticker', models.CharField(max_length=200)),
                ('longname', models.CharField(max_length=200)),
                ('shortname', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
