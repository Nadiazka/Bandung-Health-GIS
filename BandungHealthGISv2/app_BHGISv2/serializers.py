from rest_framework import serializers
from django.core.serializers import serialize
from .models import *

class KecamatanSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = Kecamatan
 		fields = ['kode_kec', 'nama_kec']

class PuskesmasSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = Puskesmas
 		fields = ['kode_pkm', 'nama_pkm']

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

			
		
