from rest_framework import serializers
from django.core.serializers import serialize
from .models import *

class ICD10_SubkategoriSerializer2(serializers.ModelSerializer):
 	class Meta:
 		model = ICD10_Subkategori
 		fields = ['subkat','nama_subkat']

class ICD10_KategoriSerializer2(serializers.ModelSerializer):
 	class Meta:
 		model = ICD10_Kategori
 		fields = ['kat','nama_kat']

class KecamatanSerializer2(serializers.ModelSerializer):
	class Meta:
		model = Kecamatan
		fields = '__all__'

class ClusteringSerializer(serializers.ModelSerializer):
	class Meta:
		model = Klaster_Penyakit
		fields = ['tanggal', 'jenis_kelamin', 'subkat', 'klaster_kode',  'klaster_nama']