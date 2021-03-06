# Generated by Django 3.0.3 on 2020-06-21 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_BHGISv2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='puskesmas',
            name='alamat',
            field=models.CharField(default=0, max_length=119),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Klaster_Penyakit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('tanggal', models.DateField()),
                ('jenis_kelamin', models.CharField(max_length=14)),
                ('jenis_kasus', models.CharField(max_length=14)),
                ('jumlah_kasus', models.PositiveSmallIntegerField()),
                ('klaster_kode', models.CharField(max_length=69)),
                ('klaster_nama', models.CharField(max_length=79)),
                ('llr', models.PositiveSmallIntegerField()),
                ('subkat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Klaster_Penyakit', to='app_BHGISv2.ICD10_Subkategori')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
