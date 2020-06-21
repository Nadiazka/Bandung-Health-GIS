from django.db import models
from softdelete.models import SoftDeleteModel


class Pasien(SoftDeleteModel):
	"""docstring for Pasien"""
	kat_pasien = models.SmallAutoField( primary_key=True)
	umur = models.CharField(max_length=10)
	jenis_kelamin = models.CharField(max_length=10)

	def __str__(self):
		return str(self.kat_pasien)

class Kecamatan(SoftDeleteModel):
	kode_kec = models.CharField(max_length=10, primary_key=True)
	nama_kec = models.CharField(max_length=25)
	lat = models.FloatField(null=True)
	longt = models.FloatField(null=True)
	pddk_l = models.PositiveIntegerField()
	pddk_p = models.PositiveIntegerField()
	jml_pddk = models.IntegerField()

	def __str__(self):
		return self.nama_kec

class Puskesmas(SoftDeleteModel):
	kode_pkm = models.CharField(max_length=13, primary_key=True)
	kode_kec = models.ForeignKey(Kecamatan, related_name='puskesmas', on_delete=models.CASCADE)
	nama_pkm = models.CharField(max_length=30)
	lat = models.FloatField(null=True)
	longt = models.FloatField(null=True)
	alamat = models.CharField(max_length=119)

	def __str__(self):
		return self.nama_pkm

class Indeks(SoftDeleteModel):
	kode = models.SmallAutoField(primary_key=True)
	kode_pkm = models.ForeignKey(Puskesmas, related_name='indeks', on_delete=models.CASCADE)
	tanggal = models.DateField()

	def __str__(self):
		return str(self.kode)
		
class ICD10_Chapter(SoftDeleteModel):
	chapter = models.CharField(max_length=7, primary_key=True)
	nama_chapter = models.CharField(max_length=149)

	def __str__(self):
		return self.nama_chapter

class ICD10_Subchapter(SoftDeleteModel):
	subchapter = models.CharField(max_length=9, primary_key=True)
	chapter = models.ForeignKey(ICD10_Chapter, related_name='icdD10_subchapter', on_delete=models.CASCADE)
	nama_subchapter = models.CharField(max_length=199)

	def __str__(self):
		return self.nama_subchapter

class ICD10_Kategori(SoftDeleteModel):
	kat = models.CharField(max_length=5, primary_key=True)
	subchapter = models.ForeignKey(ICD10_Subchapter,related_name='icd10_kategori', on_delete=models.CASCADE)
	nama_kat = models.CharField(max_length=199)

	def __str__(self):
		return self.nama_kat
						
class ICD10_Subkategori(SoftDeleteModel):
	subkat = models.CharField(max_length=9, primary_key=True)
	nama_subkat = models.CharField(max_length=100)
	kat = models.ForeignKey(ICD10_Kategori,related_name='icd10_subkategori', on_delete=models.CASCADE)
	
	def __str__(self):
		return self.nama_subkat

class Kasus(SoftDeleteModel):
	kode = models.ForeignKey(Indeks, related_name='kasus', on_delete=models.CASCADE)
	icd_10 = models.ForeignKey(ICD10_Subkategori, related_name='kasus', on_delete=models.CASCADE)
	kat_pasien = models.ForeignKey(Pasien, related_name='kasus', on_delete=models.CASCADE)
	kasus_baru = models.PositiveSmallIntegerField(blank=True)
	kasus_lama = models.PositiveSmallIntegerField(blank=True)
	jumlah = models.PositiveSmallIntegerField(blank=True)

	def __str__(self):
		return str(self.kode)

class Jumlah_Kasus_Subkat(SoftDeleteModel):
	kode = models.ForeignKey(Indeks, related_name='Jumlah_Kasus_subkat', on_delete=models.CASCADE)
	icd_10 = models.ForeignKey(ICD10_Subkategori, related_name='Jumlah_Kasus_subkat', on_delete=models.CASCADE)
	jumlah_baru_l = models.PositiveSmallIntegerField(blank=True)
	jumlah_baru_p = models.PositiveSmallIntegerField(blank=True)
	jumlah_lama_l = models.PositiveSmallIntegerField(blank=True)
	jumlah_lama_p = models.PositiveSmallIntegerField(blank=True)
	jumlah = models.PositiveSmallIntegerField(blank=True)
	gakin = models.PositiveSmallIntegerField(blank=True)

	def __str__(self):
		return str(self.kode)

class Jumlah_Kasus_Kat(SoftDeleteModel):
	kode = models.ForeignKey(Indeks, related_name='jumlah_kasus_kat', on_delete=models.CASCADE)
	kat = models.ForeignKey(ICD10_Kategori, related_name='jumlah_kasus_kat', on_delete=models.CASCADE)
	jumlah_baru_l = models.PositiveSmallIntegerField(blank=True)
	jumlah_baru_p = models.PositiveSmallIntegerField(blank=True)
	jumlah_lama_l = models.PositiveSmallIntegerField(blank=True)
	jumlah_lama_p = models.PositiveSmallIntegerField(blank=True)
	jumlah = models.PositiveSmallIntegerField(blank=True)
	gakin = models.PositiveSmallIntegerField(blank=True)

	def __str__(self):
		return str(self.kode)
		
class Jumlah_Kategori(SoftDeleteModel):
	kode = models.ForeignKey(Indeks, related_name='jumlah_kategori', on_delete=models.CASCADE)
	kat_pasien = models.ForeignKey(Pasien,null=True, related_name='jumlah_kategori', on_delete=models.CASCADE)
	kat = models.ForeignKey(ICD10_Kategori, related_name='jumlah_kategori', on_delete=models.CASCADE)
	kasus_lama = models.PositiveIntegerField(blank=True)
	kasus_baru = models.PositiveIntegerField(blank=True)
	jumlah = models.PositiveIntegerField(blank=True)
	
	def __str__(self):
		return str(self.kode)

class Jumlah_Subchapter(SoftDeleteModel):
	kode = models.ForeignKey(Indeks, related_name='jumlah_subchapter', on_delete=models.CASCADE)
	subchapter = models.ForeignKey(ICD10_Subchapter, related_name='jumlah_subchapter', on_delete=models.CASCADE)
	kat_pasien = models.ForeignKey(Pasien,null=True, related_name='jumlah_subchapter', on_delete=models.CASCADE)
	kasus_baru = models.PositiveIntegerField(blank=True)
	kasus_lama = models.PositiveIntegerField(blank=True)
	jumlah = models.PositiveIntegerField(blank=True)

	def __str__(self):
		return str(self.kode)

class Jumlah_Chapter(SoftDeleteModel):
	kode = models.ForeignKey(Indeks, related_name='jumlah_chapter', on_delete=models.CASCADE)
	chapter = models.ForeignKey(ICD10_Chapter, related_name='jumlah_chapter', on_delete=models.CASCADE)
	kat_pasien = models.ForeignKey(Pasien,null=True, related_name='jumlah_chapter', on_delete=models.CASCADE)
	kasus_baru = models.PositiveIntegerField(blank=True)
	kasus_lama = models.PositiveIntegerField(blank=True)
	jumlah = models.PositiveIntegerField(blank=True)
	
	def __str__(self):
		return str(self.kode)

class Klaster_Penyakit(SoftDeleteModel):
	tanggal = models.DateField()
	subkat = models.ForeignKey(ICD10_Subkategori, related_name='Klaster_Penyakit', on_delete=models.CASCADE)
	jenis_kelamin = models.CharField(max_length=14)
	jenis_kasus = models.CharField(max_length=14)
	jumlah_kasus = models.PositiveSmallIntegerField()
	klaster_kode = models.CharField(max_length=69)
	klaster_nama = models.CharField(max_length=79)
	llr = models.PositiveSmallIntegerField()

	def __str__(self):
		return str(self.tanggal)
