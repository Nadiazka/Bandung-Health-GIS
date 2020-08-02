from django.db.models import Q, F, Sum, Avg, Max, Min, Count
from itertools import chain
from django.http import JsonResponse
from rest_framework import generics, viewsets, status, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
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
		if len(request.FILES) != 0:
			file = request.FILES['LB1File']
			print(file)
		
			#Get pkm_code
			arr_pkmCode = xls_get(
				file,
				start_column=4, 
				start_row=3, 
				row_limit=1
				)
			list_pkmCode = list(arr_pkmCode.items())[0][1][0][0]
			print(list_pkmCode)
			split_pkmCode = list_pkmCode.split(" ")
			pkmCode = split_pkmCode[0]
			print(pkmCode)

			#Get date
			arr_date = xls_get(
				file,
				start_column=4, 
				start_row=4, 
				row_limit=1
				)
			list_date = list(arr_date.items())[0][1][0][0]
			print(list_date)
			split_date = list_date.split(" ")
			str_date = split_date[0]
			date = datetime.strptime(str_date, '%d-%m-%Y').date()
			print(date)

			#Get code
			if Indeks.objects.filter(kode_pkm=pkmCode, tanggal=date).exists()==False:
				print("create new indeks")
				Indeks.objects.create(
					kode_pkm = Puskesmas.objects.get(kode_pkm=pkmCode),
					tanggal = date
					)

			code = Indeks.objects.filter(kode_pkm=pkmCode, tanggal=date).values('kode')[0]['kode']
			print(code)

			#Get list penyakit
			obj_diseases = xls_get(
				file, 
				start_column=1, 
				column_limit=1,
				start_row=14,
				skip_empty_rows=True
				)
			diseases = list(obj_diseases.items())[0][1]

			#Get matriks kasus
			obj_case = xls_get(
				file,
				start_column=3, 
				column_limit=48,
				start_row=14,
				skip_empty_rows=True
				)
			case = list(obj_case.items())[0][1]
			
			#Get jumlah kasus
			obj_jumlahKasus = xls_get(
				file,
				start_column=51, 
				column_limit=6,
				start_row=14,
				skip_empty_rows=True
				)
			sumCase = list(obj_jumlahKasus.items())[0][1]
			print("identifikasi clear")
			#Add data in database
			if (Jumlah_Chapter.objects.filter(kode=code).exists()==False):

				for idx, disease in enumerate(diseases, start=0):
					print(idx)
					print(disease[0])

					if "." in disease[0]:
						subkat = disease[0]
						kat = ICD10_Subkategori.objects.filter(subkat=subkat).values("kat")[0]['kat']
					else :
						kat = disease[0]

					subch = ICD10_Kategori.objects.filter(kat=kat).values("subchapter")[0]['subchapter']
					ch = ICD10_Subchapter.objects.filter(subchapter=subch).values("chapter")[0]['chapter']

					print(kat)
					print(subch)
					print(ch)

					j=0
					for i in range(24):
						i += 1
						k = i+j-1
						
						if "." in disease[0]:
							Kasus.objects.create(
								kode = Indeks.objects.get(kode=code),
								icd_10 = ICD10_Subkategori.objects.get(subkat=subkat),
								kat_pasien = Pasien.objects.get(kat_pasien=i),
								kasus_baru = case[idx][k],
								kasus_lama = case[idx][k+2],
								jumlah = case[idx][k]+case[idx][k+2]
								)

						if Jumlah_Kategori.objects.filter(kode=code, kat_pasien=i, kat=kat).exists():
							print("update kat")
							Jumlah_Kategori.objects.filter(kode=code, kat_pasien=i, kat=kat)\
							.update(
								kasus_baru=F('kasus_baru') + case[idx][k],
								kasus_lama=F('kasus_lama') + case[idx][k+2],
								jumlah = F('jumlah') + case[idx][k] + case[idx][k+2]
								)
						else :
							print("create new kat")
							Jumlah_Kategori.objects.create(
							kode = Indeks.objects.get(kode=code),
							kat_pasien = Pasien.objects.get(kat_pasien=i),
							kat = ICD10_Kategori.objects.get(kat=kat),
							kasus_baru = case[idx][k],
							kasus_lama = case[idx][k+2],
							jumlah = case[idx][k] + case[idx][k+2]
							)

						if Jumlah_Subchapter.objects.filter(kode=code, kat_pasien=i, subchapter=subch).exists():
							print("update subchapter")
							Jumlah_Subchapter.objects.filter(kode=code, kat_pasien=i, subchapter=subch)\
							.update(
								kasus_baru=F('kasus_baru') + case[idx][k],
								kasus_lama=F('kasus_lama') + case[idx][k+2],
								jumlah = F('jumlah') +case[idx][k] + case[idx][k+2]
								)
						else:
							print("create new subchapter")
							Jumlah_Subchapter.objects.create(
							kode = Indeks.objects.get(kode=code),
							subchapter = ICD10_Subchapter.objects.get(subchapter=subch),
							kat_pasien = Pasien.objects.get(kat_pasien=i),
							kasus_baru = case[idx][k],
							kasus_lama = case[idx][k+2],
							jumlah = case[idx][k] + case[idx][k+2]
							)

						if Jumlah_Chapter.objects.filter(kode=code, kat_pasien=i, chapter=ch).exists():
							print("update chapter")
							Jumlah_Chapter.objects.filter(kode=code, kat_pasien=i, chapter=ch)\
							.update(
								kasus_baru=F('kasus_baru') + case[idx][k],
								kasus_lama=F('kasus_lama') + case[idx][k+2],
								jumlah = F('jumlah') +case[idx][k] + case[idx][k+2]
								)
						else:
							print("create new chapter")
							Jumlah_Chapter.objects.create(
							kode = Indeks.objects.get(kode=code),
							chapter = ICD10_Chapter.objects.get(chapter=ch),
							kat_pasien = Pasien.objects.get(kat_pasien=i),
							kasus_baru = case[idx][k],
							kasus_lama = case[idx][k+2],
							jumlah = case[idx][k] + case[idx][k+2]
							)

						if i%2 == 0 :
							j += 2

					if "." in disease[0]:
						print("create Jumlah_Kasus_Subkat")
						Jumlah_Kasus_Subkat.objects.create(
							kode = Indeks.objects.get(kode=code),
							icd_10 = ICD10_Subkategori.objects.get(subkat=subkat),
							jumlah_baru_l = sumCase[idx][0],
							jumlah_baru_p = sumCase[idx][1],
							jumlah_lama_l = sumCase[idx][2],
							jumlah_lama_p = sumCase[idx][3],
							jumlah = sumCase[idx][4],
							gakin = sumCase[idx][5]
							)

					if Jumlah_Kasus_Kat.objects.filter(kode=code, kat=kat).exists():
						print("update Jumlah_Kasus_Kat")
						Jumlah_Kasus_Kat.objects.filter(kode=code, kat=kat)\
						.update(
							jumlah_baru_l=F('jumlah_baru_l') + sumCase[idx][0], 
							jumlah_baru_p=F('jumlah_baru_p') + sumCase[idx][1],
							jumlah_lama_l=F('jumlah_lama_l') + sumCase[idx][2], 
							jumlah_lama_p=F('jumlah_lama_p') + sumCase[idx][3],
							jumlah = F('jumlah') + sumCase[idx][4],
							gakin= F('gakin') + sumCase[idx][5]
							)
					else:
						print("create new Jumlah_Kasus_Kat")
						Jumlah_Kasus_Kat.objects.create(
						kode = Indeks.objects.get(kode=code),
						kat = ICD10_Kategori.objects.get(kat=kat),
						jumlah_baru_l = sumCase[idx][0],
						jumlah_baru_p = sumCase[idx][1],
						jumlah_lama_l = sumCase[idx][2],
						jumlah_lama_p = sumCase[idx][3],
						jumlah = sumCase[idx][4],
						gakin = sumCase[idx][5]
						)

				#Clustering
				countPkm = Indeks.objects.filter(tanggal=date)\
				.annotate(Count('kode_pkm', distinct=True))
				if countPkm>60 :
					funcClustering(date)

			print("Done")
			print(list_pkmCode)
			print(date)
			print(len(diseases))
			print(len(diseases)*24)

			fs = FileSystemStorage()
			filename = fs.save(file.name, file)
			uploaded_file_url = fs.url(filename)
			return redirect('index')

		else:
			return redirect('index')

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
		qsClustering = Klaster_Penyakit.objects.select_related('subkat')\
		.order_by('-llr')[:3].values('subkat__nama_subkat','klaster_kode', 'klaster_nama', 'llr')
		qsChartKasus = qs.aggregate(Kasus_Baru=Sum('kasus_baru'), Kasus_Lama=Sum('kasus_lama'))

		if is_valid_queryparam(penyakit_query) and penyakit_query!= "Semua Penyakit":
			splitKodePenyakit = penyakit_query.split(":")
			kodePenyakit = splitKodePenyakit[0]

			if "." in kodePenyakit:
				qs = Kasus.objects.select_related('kode__kode_pkm')\
				.filter(icd_10=kodePenyakit)
			else:
				qs = Jumlah_Kategori.objects.select_related('kode__kode_pkm')\
				.filter(kat=kodePenyakit)

			#Clustering
			qsClustering = Klaster_Penyakit.objects\
			.select_related('subkat')\
			.filter(
				tanggal__gte=dateStart_query,
				tanggal__lt=dateEnd_query,
				subkat=kodePenyakit,
				jenis_kelamin=gender_query
				)\
			.order_by('-llr')[:3]\
			.values(
				'subkat',
				'subkat__nama_subkat',
				'jenis_kelamin',
				'tanggal',
				'klaster_kode',
				'klaster_nama',
				'llr')

		elif penyakit_query == "Semua Penyakit":
			qs = Jumlah_Chapter.objects.select_related('kode__kode_pkm')
			
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
			tempEndDate = datetime.strptime(dateEnd_query, '%Y-%m-%d').date()
			endPeriode = last_day_of_month(tempEndDate)

		if is_valid_queryparam(jenisKasus_query):
			if jenisKasus_query=="Kasus Baru":
				qsPkm = qs.values('kode__kode_pkm', 'kode__kode_pkm__nama_pkm').annotate(kasus = Sum('kasus_baru'))
				qsKec = qs.values('kode__kode_pkm__kode_kec', 'kode__kode_pkm__kode_kec__nama_kec').annotate(kasus = Sum('kasus_baru'))
				qsChartUmur = qs.values('kat_pasien__umur').annotate(kasus = Sum('kasus_baru')).order_by('-kasus')[:10]
				qsChartGender =qs.values('kat_pasien__jenis_kelamin').annotate(kasus = Sum('kasus_baru'))
				qsChartDate =qs.values('kode__tanggal').annotate(kasus = Sum('kasus_baru')).order_by('-kode__tanggal')[:10]
				qsChartKasus = qs.aggregate(Kasus_Baru=Sum('kasus_baru'))
			elif jenisKasus_query=="Kasus Lama":
				qsPkm = qs.values('kode__kode_pkm', 'kode__kode_pkm__nama_pkm').annotate(kasus = Sum('kasus_lama'))
				qsKec = qs.values('kode__kode_pkm__kode_kec', 'kode__kode_pkm__kode_kec__nama_kec').annotate(kasus = Sum('kasus_lama'))
				qsChartUmur = qs.values('kat_pasien__umur').annotate(kasus = Sum('kasus_lama')).order_by('-kasus')[:10]
				qsChartGender =qs.values('kat_pasien__jenis_kelamin').annotate(kasus = Sum('kasus_lama'))
				qsChartDate =qs.values('kode__tanggal').annotate(kasus = Sum('kasus_lama')).order_by('-kode__tanggal')[:10]
				qsChartKasus = qs.aggregate(Kasus_Lama=Sum('kasus_lama'))
			elif jenisKasus_query=="Semua Jenis":
				qsPkm = qs.values('kode__kode_pkm', 'kode__kode_pkm__nama_pkm').annotate(kasus=Sum('jumlah'))
				qsKec = qs.values('kode__kode_pkm__kode_kec', 'kode__kode_pkm__kode_kec__nama_kec').annotate(kasus=Sum('jumlah'))
				qsChartUmur = qs.values('kat_pasien__umur').annotate(kasus=Sum('jumlah')).order_by('-kasus')[:10]
				qsChartGender =qs.values('kat_pasien__jenis_kelamin').annotate(kasus=Sum('jumlah'))
				qsChartDate =qs.values('kode__tanggal').annotate(kasus=Sum('jumlah')).order_by('-kode__tanggal')[:10]
				qsChartKasus = qs.aggregate(Kasus_Baru=Sum('kasus_baru'), Kasus_Lama=Sum('kasus_lama'))
		
			if penyakit_query!= "Semua Penyakit" and "." in kodePenyakit:
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
			'chartKasus' : qsChartKasus,
			'qsClustering' : list(qsClustering),
			'qs' :query
		}
		return render (request, 'app_BHGIS/indexV2.html', data)

	return render (request, 'app_BHGIS/indexV2.html')

def funcClustering(tgl):
	#urlOutput = requests.get('https://djatianwar.shinyapps.io/disease-clustering/')
	#dataOutput = urlOutput.json()
	dataOutput ={}
	if len(dataOutput) > 0:
		tanggal = dataOutput[0].tanggal
		if Klaster_Penyakit.objects.filter(tanggal=tanggal).exists()==False:
			for data in dataOutput:
				Klaster_Penyakit.objects.create(
					tanggal=data.tanggal,
					subkat=ICD10_Subkategori.objects.get(subkat=data.subkat),
					jenis_kelamin=data.jenis_kelamin,
					jumlah_kasus=data.kasus,
					klaster_kode=data.klaster_kode,
					klaster_nama=data.klaster_nama,
					jumlah_populasi = data.jumlah_populasi,
					ekspektasi_kasus = data.ekspektasi_kasus,
					smr = data.smr,
					llr=data.llr,
					rank = data.rank,
					p_value = data.p_value
					)
	tanggal = Indeks.objects.values('tanggal').order_by('tanggal')[0]['tanggal']
	qsLooping = Jumlah_Kasus_Subkat.objects.select_related('kode__kode_pkm')\
		.filter(kode__tanggal=tanggal)\
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

class DataClustering(generics.ListCreateAPIView):
	queryset = Kecamatan.objects.all()
	serializer_class = KecamatanSerializer2
		
class PenyakitSubkat(generics.ListCreateAPIView):
	queryset = ICD10_Subkategori.objects.values('subkat','nama_subkat')
	serializer_class = ICD10_SubkategoriSerializer2

class PenyakitKat(generics.ListCreateAPIView):
	queryset = ICD10_Kategori.objects.values('kat','nama_kat')
	serializer_class = ICD10_KategoriSerializer2