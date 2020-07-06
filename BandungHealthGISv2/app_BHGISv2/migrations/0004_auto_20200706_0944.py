# Generated by Django 3.0.3 on 2020-07-06 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_BHGISv2', '0003_auto_20200624_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kecamatan',
            name='lat',
            field=models.CharField(default=0, max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='kecamatan',
            name='longt',
            field=models.CharField(default=0, max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='klaster_penyakit',
            name='p_value',
            field=models.FloatField(max_length=5),
        ),
        migrations.AlterField(
            model_name='klaster_penyakit',
            name='rank',
            field=models.FloatField(max_length=2),
        ),
        migrations.AlterField(
            model_name='klaster_penyakit',
            name='smr',
            field=models.FloatField(max_length=2),
        ),
    ]
