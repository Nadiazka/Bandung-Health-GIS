from django.db.models import Q, F, Sum, Avg, Max, Min, Count
from itertools import chain
from django.http import JsonResponse
from rest_framework import generics, viewsets, status, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.views.generic import View, ListView
from .models import *
from django.contrib.auth.decorators import login_required
from .serializers import *
from django.http import HttpResponse
import json
import django_excel as excel
import pyexcel as pe
from pyexcel_xls import get_data as xls_get 
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import sys
from collections import OrderedDict
from calendar import monthrange
import requests

def is_valid_queryparam(param):
	return param != '' and param is not None

def last_day_of_month(date_value):
    return date_value.replace(day = monthrange(date_value.year, date_value.month)[1])

# Create your views here.
@login_required(login_url='login')
def index(request):
	print("oke")
	if request.method == 'POST':
		file = request.FILES['LB1File']
		print(file)
	
		#Get pkm_code
		arr_pkmCode = xls_get(
			file,
			start_column=4, 
			start_row=3, 
			row_limit=1
			)
		list_pkmCode = list(arr_pkmCode.items())
		val_pkmCode = list_pkmCode[0][1][0][0]
		print(val_pkmCode)
		split_pkmCode = val_pkmCode.split(" ")
		pkmCode = split_pkmCode[0]
		print(pkmCode)

		#Get date
		arr_date = xls_get(
			file,
			start_column=4, 
			start_row=4, 
			row_limit=1
			)
		list_date = list(arr_date.items())
		val_date = list_date[0][1][0][0]
		print(val_date)
		split_date = val_date.split(" ")
		str_date = split_date[0]
		date = datetime.strptime(str_date, '%d-%m-%Y').date()
		print(date)

		#Get code
		if Indeks.objects.filter(kode_pkm=pkmCode, tanggal=date).exists()==False:
			print("create new indeks")
			Indeks.objects.create(
				kode_pkm = Puskesmas.objects.get(kode_pkm=pkmCode),
				tanggal = date,
				deleted = 0
				)

		qs_code = Indeks.objects.filter(kode_pkm=pkmCode, tanggal=date).values('kode')
		print(qs_code)
		code = qs_code[0]['kode'] 
		print(code)

		#Get list penyakit
		obj_diseases = xls_get(
			file, 
			start_column=1, 
			column_limit=1,
			start_row=14,
			skip_empty_rows=True
			)
		list_diseases = list(obj_diseases.items())
		diseases = list_diseases[0][1]

		#Get matriks kasus
		obj_case = xls_get(
			file,
			start_column=3, 
			column_limit=48,
			start_row=14,
			skip_empty_rows=True
			)
		list_case = list(obj_case.items())
		case = list_case[0][1]

		#Get gakin
		obj_gakin = xls_get(
			file,
			start_column=56, 
			column_limit=1,
			start_row=14,
			skip_empty_rows=True
			)
		gakin = list(obj_gakin.items())[0][1]

		#Add data in database
		if (Kasus.objects.filter(kode=code).exists()==False) and (Jumlah_Kategori.objects.filter(kode=code).exists()==False):

			for idx, disease in enumerate(diseases, start=0):
				print(idx)
				print(disease[0])
				j=0
				for i in range(24):
					i += 1
					k = i+j-1
					
					
					if ICD10_Kategori.objects.filter(kat=disease[0]).exists() :
						print("database kategori")
						kat = disease[0]
						Jumlah_Kategori.objects.create(
							kode = Indeks.objects.get(kode=code),
							kat_pasien = Pasien.objects.get(kat_pasien=i),
							kat = ICD10_Kategori.objects.get(kat=kat),
							jumlah_kat_baru = case[idx][k],
							jumlah_kat_lama = case[idx][k+2],
							jumlah_kat = case[idx][k] + case[idx][k+2]
							)					
					elif ICD10_Subkategori.objects.filter(subkat=disease[0]).exists():
						print("database subkat")
						Kasus.objects.create(
							kode = Indeks.objects.get(kode=code),
							icd_10 = ICD10_Subkategori.objects.get(subkat=disease[0]),
							kat_pasien = Pasien.objects.get(kat_pasien=i),
							kasus_baru = case[idx][k],
							kasus_lama = case[idx][k+2]
							)
						kat = ICD10_Subkategori.objects.filter(subkat=disease[0]).values("kat")[0]['kat']
						print (kat)

						if Jumlah_Kategori.objects.filter(kode=code, kat_pasien=i, kat=kat).exists():
							print("update kat")
							Jumlah_Kategori.objects.filter(kode=code, kat_pasien=i, kat=kat)\
							.update(
								jumlah_kat_baru=F('jumlah_kat_baru') + case[idx][k],
								jumlah_kat_lama=F('jumlah_kat_lama') + case[idx][k+2],
								jumlah_kat = F('jumlah_kat') +case[idx][k] + case[idx][k+2]
								)
						else:
							print("create new kat")
							Jumlah_Kategori.objects.create(
							kode = Indeks.objects.get(kode=code),
							kat_pasien = Pasien.objects.get(kat_pasien=i),
							kat = ICD10_Kategori.objects.get(kat=kat),
							jumlah_kat_baru = case[idx][k],
							jumlah_kat_lama = case[idx][k+2],
							jumlah_kat = case[idx][k] + case[idx][k+2]
							)
						
					subch = ICD10_Kategori.objects.filter(kat=kat).values("subchapter")[0]['subchapter']
					ch = ICD10_Subchapter.objects.filter(subchapter=subch).values("chapter")[0]['chapter']
					print(subch)
					print(ch)

					if Jumlah_Subchapter.objects.filter(kode=code, kat_pasien=i, subchapter=subch).exists():
						print("update subchapter")
						Jumlah_Subchapter.objects.filter(kode=code, kat_pasien=i, subchapter=subch)\
						.update(
							jumlah_subchapter_baru=F('jumlah_subchapter_baru') + case[idx][k],
							jumlah_subchapter_lama=F('jumlah_subchapter_lama') + case[idx][k+2],
							jumlah_subchapter = F('jumlah_subchapter') +case[idx][k] + case[idx][k+2]
							)
					else:
						print("create new subchapter")
						Jumlah_Subchapter.objects.create(
						kode = Indeks.objects.get(kode=code),
						subchapter = ICD10_Subchapter.objects.get(subchapter=subch),
						kat_pasien = Pasien.objects.get(kat_pasien=i),
						jumlah_subchapter_baru = case[idx][k],
						jumlah_subchapter_lama = case[idx][k+2],
						jumlah_subchapter = case[idx][k] + case[idx][k+2]
						)

					if Jumlah_Chapter.objects.filter(kode=code, kat_pasien=i, chapter=ch).exists():
						print("update chapter")
						Jumlah_Chapter.objects.filter(kode=code, kat_pasien=i, chapter=ch)\
						.update(
							jumlah_chapter_baru=F('jumlah_chapter_baru') + case[idx][k],
							jumlah_chapter_lama=F('jumlah_chapter_lama') + case[idx][k+2],
							jumlah_chapter = F('jumlah_chapter') +case[idx][k] + case[idx][k+2]
							)
					else:
						print("create new chapter")
						Jumlah_Chapter.objects.create(
						kode = Indeks.objects.get(kode=code),
						chapter = ICD10_Chapter.objects.get(chapter=ch),
						kat_pasien = Pasien.objects.get(kat_pasien=i),
						jumlah_chapter_baru = case[idx][k],
						jumlah_chapter_lama = case[idx][k+2],
						jumlah_chapter = case[idx][k] + case[idx][k+2]
						)

					if i%2 == 0 :
						j += 2

				if ICD10_Kategori.objects.filter(kat=disease[0]).exists() :
					qs_jkkbl = Jumlah_Kategori.objects\
					.filter(kode=code, kat=disease[0] ,kat_pasien__jenis_kelamin="laki-laki")\
					.aggregate(kasus = Sum('jumlah_kat_baru'))
					jkkbl = qs_jkkbl['kasus']
					qs_jkkbp = Jumlah_Kategori.objects\
					.filter(kode=code, kat=disease[0] ,kat_pasien__jenis_kelamin="perempuan")\
					.aggregate(kasus = Sum('jumlah_kat_baru'))
					jkkbp = qs_jkkbp['kasus']
					qs_jkkll = Jumlah_Kategori.objects\
					.filter(kode=code, kat=disease[0] ,kat_pasien__jenis_kelamin="laki-laki")\
					.aggregate(kasus = Sum('jumlah_kat_lama'))
					jkkll = qs_jkkll['kasus']
					qs_jkklp = Jumlah_Kategori.objects\
					.filter(kode=code, kat=disease[0] ,kat_pasien__jenis_kelamin="perempuan")\
					.aggregate(kasus = Sum('jumlah_kat_lama'))
					jkklp = qs_jkklp['kasus']

					print("Jumlah_Kasus_Kat")
					Jumlah_Kasus_Kat.objects.create(
						kode = Indeks.objects.get(kode=code),
						kat = ICD10_Kategori.objects.get(kat=disease[0]),
						jumlah_baru_l = jkkbl,
						jumlah_baru_p = jkkbp,
						jumlah_lama_l = jkkll,
						jumlah_lama_p = jkklp,
						jumlah = jkkbl + jkkbp + jkkll + jkklp,
						gakin = gakin[idx][0]
						)

				elif ICD10_Subkategori.objects.filter(subkat=disease[0]).exists():	
					qs_jksbl = Kasus.objects\
					.filter(kode=code, icd_10=disease[0] ,kat_pasien__jenis_kelamin="laki-laki")\
					.aggregate(kasus = Sum('kasus_baru'))
					jksbl = qs_jksbl['kasus']
					qs_jksbp = Kasus.objects\
					.filter(kode=code, icd_10=disease[0] ,kat_pasien__jenis_kelamin="perempuan")\
					.aggregate(kasus = Sum('kasus_baru'))
					jksbp = qs_jksbp['kasus']
					qs_jksll = Kasus.objects\
					.filter(kode=code, icd_10=disease[0] ,kat_pasien__jenis_kelamin="laki-laki")\
					.aggregate(kasus = Sum('kasus_lama'))
					jksll = qs_jksll['kasus']
					qs_jkslp = Kasus.objects\
					.filter(kode=code, icd_10=disease[0] ,kat_pasien__jenis_kelamin="perempuan")\
					.aggregate(kasus = Sum('kasus_lama'))
					jkslp = qs_jkslp['kasus']

					print("create Jumlah_Kasus_Subkat")
					Jumlah_Kasus_Subkat.objects.create(
						kode = Indeks.objects.get(kode=code),
						icd_10 = ICD10_Subkategori.objects.get(subkat=disease[0]),
						jumlah_baru_l = jksbl,
						jumlah_baru_p = jksbp,
						jumlah_lama_l = jksll,
						jumlah_lama_p = jkslp,
						jumlah = jksbl + jksbp + jksll + jkslp,
						gakin = gakin[idx][0]
						)

					kat = ICD10_Subkategori.objects.filter(subkat=disease[0]).values("kat")[0]['kat']
					if Jumlah_Kasus_Kat.objects.filter(kode=code, kat=kat).exists():
						print("update Jumlah_Kasus_Kat")
						Jumlah_Kasus_Kat.objects.filter(kode=code, kat=kat)\
						.update(
							jumlah_baru_l=F('jumlah_baru_l') + jksbl, 
							jumlah_baru_p=F('jumlah_baru_p') + jksbp,
							jumlah_lama_l=F('jumlah_lama_l') + jksll, 
							jumlah_lama_p=F('jumlah_lama_p') + jkslp,
							jumlah = F('jumlah') + jksbl + jksbp + jksll + jkslp
							)
					else:
						print("create new Jumlah_Kasus_Kat")
						Jumlah_Kasus_Kat.objects.create(
						kode = Indeks.objects.get(kode=code),
						kat = ICD10_Kategori.objects.get(kat=kat),
						jumlah_baru_l = jksbl,
						jumlah_baru_p = jksbp,
						jumlah_lama_l = jksll,
						jumlah_lama_p = jkslp,
						jumlah = jksbl + jksbp + jksll + jkslp,
						gakin = gakin[idx][0]
						)

		#Clustering
		countPkm = Indeks.objects.select_related('kode__kode_pkm')\
		.filter(tanggal=date).annotate(Count('kode__kode_pkm', distinct=True))
		if countPkm>60 :
			funcClustering(date)

		print("Done")
		print(val_pkmCode)
		print(val_date)
		print(len(diseases))
		print(len(diseases)*24)

		fs = FileSystemStorage()
		filename = fs.save(file.name, file)
		uploaded_file_url = fs.url(filename)
		return render(request, 'app_BHGIS/indexV2.html', {
            'urlFile': uploaded_file_url
        })

	elif request.method == 'GET':
		penyakit_query = request.GET.get("Penyakit")
		gender_query = request.GET.get('JenisKelamin')
		umur_query = request.GET.get('Umur')
		dateStart_query = request.GET.get('dateStart')
		dateEnd_query = request.GET.get('dateEnd')
		jenisKasus_query = request.GET.get('JenisKasus')
		
		print(penyakit_query)
		print(gender_query)
		print(umur_query)
		print(dateStart_query)
		print(dateEnd_query)
		print(jenisKasus_query)

		#Tampilan Default
		#Get last date in database
		startPeriode = Indeks.objects.values('tanggal').order_by('-tanggal')[0]['tanggal']
		print(startPeriode)
		#get last date in the last month
		endPeriode = last_day_of_month(startPeriode)

		qs = Jumlah_Kategori.objects.select_related('kode__kode_pkm').filter(kode__tanggal=startPeriode)
		qsPkm = qs.values('kode__kode_pkm', 'kode__kode_pkm__nama_pkm')\
				.annotate(kasus = Sum('kasus_baru'))
		qsKec = qs.values('kode__kode_pkm__kode_kec', 'kode__kode_pkm__kode_kec__nama_kec')\
				.annotate(kasus = Sum('kasus_baru'))
		qsChartPenyakit = qs.values('kat__nama_kat')\
				.annotate(kasus = Sum('kasus_baru'))\
				.order_by('kasus')[:10]
		qsChartUmur = qs.values('kat_pasien__umur').annotate(kasus = Sum('kasus_baru')).order_by('-kasus')[:10]
		qsChartGender =qs.values('kat_pasien__jenis_kelamin').annotate(kasus = Sum('kasus_baru'))
		qsChartDate =qs.values('kode__tanggal').annotate(kasus = Sum('kasus_baru')).order_by('-kasus')[:10]

		if is_valid_queryparam(penyakit_query):
			if ICD10_Kategori.objects.filter(nama_kat__iexact=penyakit_query).exists():
				kodePenyakit = ICD10_Kategori.objects.filter(nama_kat__iexact=penyakit_query).values('kat')[0]['kat']
			elif ICD10_Subkategori.objects.filter(nama_subkat__iexact=penyakit_query).exists():
				kodePenyakit = ICD10_Subkategori.objects.filter(nama_subkat__iexact=penyakit_query).values('subkat')[0]['subkat']
			else:
				kodePenyakit = "Semua Penyakit"
			print(kodePenyakit)

			if kodePenyakit == "Semua Penyakit" :
				qs = Jumlah_Kategori.objects.select_related('kode__kode_pkm')
			elif "." in kodePenyakit:
				qs = Kasus.objects.select_related('kode__kode_pkm')\
				.filter(icd_10=kodePenyakit)
			else:
				qs = Jumlah_Kategori.objects.select_related('kode__kode_pkm')\
				.filter(kat=kodePenyakit)
		
		if is_valid_queryparam(gender_query) and gender_query != "Semua Jenis":
			qs = qs.filter(kat_pasien__jenis_kelamin__iexact=gender_query)

		if is_valid_queryparam(umur_query) and umur_query != "Semua Umur":
			qs = qs.filter(kat_pasien__umur__iexact=umur_query)

		if is_valid_queryparam(dateStart_query):
			qs = qs.filter(kode__tanggal__gte=dateStart_query)
			tempStartDate = datetime.strptime(dateStart_query, '%Y-%m-%d').date()
			startPeriode = tempStartDate

		if is_valid_queryparam(dateEnd_query):
			qs = qs.filter(kode__tanggal__lt=dateEnd_query)
			tempEndDate = Indeks.objects.filter(tanggal__lt=dateEnd_query)\
			.order_by('-tanggal')[0]['tanggal']
			#tempEndDate2 = datetime.strptime(tempEndDate1, '%Y-%m-%d').date()
			endPeriode = last_day_of_month(tempEndDate)

		if is_valid_queryparam(jenisKasus_query):
			if jenisKasus_query=="Kasus Baru":
				qsPkm = qs.values('kode__kode_pkm', 'kode__kode_pkm__nama_pkm').annotate(kasus = Sum('kasus_baru'))
				qsKec = qs.values('kode__kode_pkm__kode_kec', 'kode__kode_pkm__kode_kec__nama_kec').annotate(kasus = Sum('kasus_baru'))
				qsChartUmur = qs.values('kat_pasien__umur').annotate(kasus = Sum('kasus_baru')).order_by('-kasus')[:10]
				qsChartGender =qs.values('kat_pasien__jenis_kelamin').annotate(kasus = Sum('kasus_baru'))
				qsChartDate =qs.values('kode__tanggal').annotate(kasus = Sum('kasus_baru')).order_by('kasus')[:10]
			elif jenisKasus_query=="Kasus Lama":
				qsPkm = qs.values('kode__kode_pkm', 'kode__kode_pkm__nama_pkm').annotate(kasus = Sum('kasus_lama'))
				qsKec = qs.values('kode__kode_pkm__kode_kec', 'kode__kode_pkm__kode_kec__nama_kec').annotate(kasus = Sum('kasus_lama'))
				qsChartUmur = qs.values('kat_pasien__umur').annotate(kasus = Sum('kasus_lama')).order_by('-kasus')[:10]
				qsChartGender =qs.values('kat_pasien__jenis_kelamin').annotate(kasus = Sum('kasus_lama'))
				qsChartDate =qs.values('kode__tanggal').annotate(kasus = Sum('kasus_lama')).order_by('kasus')[:10]
			elif jenisKasus_query=="Semua Jenis":
				qsPkm = qs.values('kode__kode_pkm', 'kode__kode_pkm__nama_pkm').annotate(kasus=Sum('jumlah'))
				qsKec = qs.values('kode__kode_pkm__kode_kec', 'kode__kode_pkm__kode_kec__nama_kec').annotate(kasus=Sum('jumlah'))
				qsChartUmur = qs.values('kat_pasien__umur').annotate(kasus=Sum('jumlah')).order_by('-kasus')[:10]
				qsChartGender =qs.values('kat_pasien__jenis_kelamin').annotate(kasus=Sum('jumlah'))
				qsChartDate =qs.values('kode__tanggal').annotate(kasus=Sum('jumlah')).order_by('kasus')[:10]
		
			if "." in kodePenyakit:
				if jenisKasus_query == "Kasus Baru":
					qsChartPenyakit = qs.values('icd_10__nama_subkat').annotate(kasus = Sum('kasus_baru')).order_by('kasus')[:10]
				elif jenisKasus_query=="Kasus Lama":
					qsChartPenyakit = qs.values('icd_10__nama_subkat').annotate(kasus = Sum('kasus_lama')).order_by('kasus')[:10]
				elif jenisKasus_query=="Semua Jenis":
					qsChartPenyakit = qs.values('icd_10__nama_subkat').annotate(kasus=Sum('jumlah')).order_by('kasus')[:10]
			else:
				if jenisKasus_query == "Kasus Baru":
					qsChartPenyakit = qs.values('kat__nama_kat').annotate(kasus = Sum('kasus_baru')).order_by('kasus')[:10]
				elif jenisKasus_query=="Kasus Lama":
					qsChartPenyakit = qs.values('kat__nama_kat').annotate(kasus = Sum('kasus_lama')).order_by('kasus')[:10]
				elif jenisKasus_query=="Semua Jenis":
					qsChartPenyakit = qs.values('kat__nama_kat').annotate(kasus=Sum('jumlah')).order_by('kasus')[:10]

		qsChartPkm = qsPkm.order_by('-kasus')[:10]
		qsChartKec = qsKec.order_by('-kasus')[:10]
		distNormPkm = qsPkm.aggregate(Max('kasus'), Min('kasus'))
		distNormKec = qsKec.aggregate(Max('kasus'), Min('kasus'))

		#Clustering
		if kodePenyakit != "Semua Penyakit":
			qsClustering = Klaster_Penyakit.objects\
			.filter(
				tanggal__gte=dateStart_query,
				tanggal__lt=dateEnd_query,
				subkat__icontains=kodePenyakit,
				jenis_kelamin=gender_query,
				jenis_kasus=jenisKasus_query
				)\
			.order_by('-llr')[:3]\
			.values('subkat','klaster_kode', 'klaster_nama', 'llr')

		startPeriode = startPeriode.strftime('%d/%m/%y')
		endPeriode= endPeriode.strftime('%d/%m/%y')
		
		#Informasi legenda di map
		query = {
			'penyakit_query': penyakit_query,
			'gender_query':gender_query,
			'umur_query': umur_query,
			'jenisKasus_query':jenisKasus_query,
			'startPeriode' :startPeriode,
			'endPeriode': endPeriode
		}
		data ={
			'areaPkm' : list(qsPkm),
			'areaKec' : list(qsKec),
			'statPkm' : distNormPkm,
			'statKec' : distNormKec,
			'chartPkm' : list(qsChartPkm),
			'chartKec' : list(qsChartKec),
			'chartPenyakit' : list(qsChartPenyakit),
			'chartGender' : list(qsChartGender),
			'chartUmur' : list(qsChartUmur),
			'chartPeriode' : list(qsChartDate),
			'qsClustering' : list(qsClustering),
			'qs' :query
		}
		return render (request, 'app_BHGIS/indexV2.html', data)

	return render (request, 'app_BHGIS/indexV2.html')

class dataFiltering(View):
	def get(self, request):
		return JsonResponse(iClustering)

def funcClustering(tgl):
	#urlOutput = requests.get('https://ssdsd')
	#dataOutput = urlOutput.json()
	dataOutput ={} 
	if dataOutput is not None:
		tanggal = dataOutput[0].tanggal
		if Klaster_Penyakit.objects.filter(tanggal=tanggal).exists()==False:
			for data in dataOutput:
				Klaster_Penyakit.objects.create(
					tanggal=data.tanggal,
					subkat=ICD10_Subkategori.objects.get(subkat=data.subkat),
					jenis_kelamin=data.jenis_kelamin,
					jenis_kasus=data.jenis_kasus,
					jumlah_kasus=data.kasus,
					klaster_kode=data.klaster_kode,
					klaster_nama=data.klaster_nama,
					llr=data.llr
					)

	qsLooping = Jumlah_Kasus_Subkat.objects.select_related('kode__kode_pkm')\
		.filter(kode__tanggal=tgl)\
		.values('kode__tanggal', 'kode__kode_pkm__kode_kec', 'icd_10')\
		.annotate(
			baru_l=Sum('jumlah_baru_l'),
			baru_p=Sum('jumlah_baru_p'), 
			lama_l=Sum('jumlah_lama_l'), 
			lama_p=Sum('jumlah_lama_p'), 
			baru=Sum(F('jumlah_baru_l')+F('jumlah_baru_p')), 
			lama=Sum(F('jumlah_lama_l')+F('jumlah_lama_p')), 
			l=Sum(F('jumlah_baru_l')+F('jumlah_lama_l')), 
			p=Sum(F('jumlah_baru_p')+F('jumlah_lama_p')), 
			jumlah=Sum('jumlah'))
	data ={
		'qsHasil' : list(qsLooping)
	}
	return JsonResponse(data)

		
def get_data(request):
	"""
	data = Kasus.objects.select_related('kode__kode_pkm')\
	.values('kode__kode_pkm', 'kode__kode_pkm__nama_pkm')\
	.annotate(kasus = Sum('kasus_baru'))
	response = json.dumps(list(data))
	"""
	response = json.dumps(list(qsFiltering))
	return HttpResponse(response)

class DataClustering(View):
	def get(self, request):
		#qsGeodict = Kecamatan.objects.values('kode_kec', 'nama_kec', 'lat', 'longt')
		#qsDatadict = Kecamatan.objects.values('kode_kec', 'nama_kec', 'jml_pddk', 'pddk_l', 'pddk_p')
		qsSubkat = ICD10_Subkategori.objects.values('subkat')
		tgl = Indeks.objects.values('tanggal').order_by('tanggal').distinct()[11]['tanggal']
		qsLooping = Jumlah_Kasus_Subkat.objects.select_related('kode__kode_pkm')\
		.filter(kode__tanggal=tgl)\
		.values('kode__tanggal', 'kode__kode_pkm__kode_kec', 'icd_10')\
		.annotate(
			baru_l=Sum('jumlah_baru_l'),
			baru_p=Sum('jumlah_baru_p'), 
			lama_l=Sum('jumlah_lama_l'), 
			lama_p=Sum('jumlah_lama_p'), 
			baru=Sum(F('jumlah_baru_l')+F('jumlah_baru_p')), 
			lama=Sum(F('jumlah_lama_l')+F('jumlah_lama_p')), 
			l=Sum(F('jumlah_baru_l')+F('jumlah_lama_l')), 
			p=Sum(F('jumlah_baru_p')+F('jumlah_lama_p')), 
			jumlah=Sum('jumlah'))
		data ={
			#'Geodict' : list(qsGeodict),
			#'Datadict' : list(qsDatadict),
			#'Subkat' : list(qsSubkat),
			'qsHasil' : list(qsLooping)
		}
		return JsonResponse(data)
		
class PenyakitSubkat(generics.ListCreateAPIView):
	queryset = ICD10_Subkategori.objects.values('nama_subkat')
	serializer_class = ICD10_SubkategoriSerializer2

class PenyakitKat(generics.ListCreateAPIView):
	queryset = ICD10_Kategori.objects.values('nama_kat')
	serializer_class = ICD10_KategoriSerializer2

class Puskesmas(generics.ListCreateAPIView):
	queryset = Puskesmas.objects.values('kode_pkm', 'nama_pkm').order_by('nama_pkm')
	serializer_class = PuskesmasSerializer

class Kecamatan(generics.ListCreateAPIView):
	queryset = Kecamatan.objects.values('kode_kec', 'nama_kec').order_by('nama_kec')
	serializer_class = KecamatanSerializer