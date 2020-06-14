from rest_framework import serializers
from django.core.serializers import serialize
from .models import *

class PasienSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = Pasien
 		fields = '__all__'

class KecamatanSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = Kecamatan
 		fields = ['kode_kec', 'nama_kec']

class PuskesmasSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = Puskesmas
 		fields = ['kode_pkm', 'nama_pkm']

class KasusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Kasus
		fields = '__all__'
		depth = 4

class JumlahKategoriSerializer(serializers.ModelSerializer):
	class Meta:
		model = Jumlah_Kategori
		fields = '__all__'
		depth = 4

class IndeksSerializer(serializers.ModelSerializer):
	kasus = KasusSerializer(many=True)
	jumlah_kategori = JumlahKategoriSerializer(many=True)

	class Meta:
		model = Indeks
		fields = ['kasus','jumlah_kategori']

class PetaPkmSerializer(serializers.ModelSerializer):
	indeks = IndeksSerializer(many=True)

	class Meta:
		model =  Puskesmas
		fields = ['kode_pkm', 'nama_pkm', 'indeks']

class ICD10_ChapterSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = ICD10_Chapter
 		fields = '__all__'

class ICD10_SubchapterSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = ICD10_Subchapter
 		fields = '__all__'

class ICD10_KategoriSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = ICD10_Kategori
 		fields = '__all__'

class ICD10_SubkategoriSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = ICD10_Subkategori
 		fields = '__all__'
 		depth = 3

class ICD10_SubkategoriSerializer2(serializers.ModelSerializer):
 	class Meta:
 		model = ICD10_Subkategori
 		fields = ['nama_subkat']

class ICD10_KategoriSerializer2(serializers.ModelSerializer):
 	class Meta:
 		model = ICD10_Kategori
 		fields = ['nama_kat']

class OptionPkm(serializers.ModelSerializer):
	class Meta:
		model = Puskesmas
		fields =['nama_pkm']
			
		
