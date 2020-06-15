from django.db.models import Q, F, Sum, Avg, Max, Min
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
"""
import rpy2.robjects as ro
import rpy2.robjects.packages as rpackages
import pandas as pd
import numpy as np
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.vectors import StrVector
from rpy2.robjects import NULL
"""
def is_valid_queryparam(param):
	return param != '' and param is not None

iClustering = {}
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

		print("Done")
		print(list_pkmCode)
		print(date)
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
		#lastDate = Indeks.objects.values('tanggal').order_by('-tanggal')[0]['tanggal']
		date = datetime.strptime('01-10-2019', '%d-%m-%Y').date()
		lastDate = Indeks.objects.filter(tanggal=date).values('tanggal')[0]['tanggal']
		print(lastDate)
		qs = Jumlah_Kategori.objects.select_related('kode__kode_pkm').filter(kode__tanggal=lastDate)
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
			
			if ICD10_Kategori.objects.filter(kat__iexact=kodePenyakit).exists():
				qs = Jumlah_Kategori.objects.select_related('kode__kode_pkm')\
				.filter(kat=kodePenyakit)
			elif ICD10_Subkategori.objects.filter(subkat__iexact=kodePenyakit).exists():
				qs = Kasus.objects.select_related('kode__kode_pkm')\
				.filter(icd_10=kodePenyakit)
			else: #Semua Jenis
				qs = Jumlah_Kategori.objects.select_related('kode__kode_pkm')
		
		if is_valid_queryparam(gender_query) and gender_query != "Semua Jenis":
			qs = qs.filter(kat_pasien__jenis_kelamin__iexact=gender_query)

		if is_valid_queryparam(umur_query) and umur_query != "Semua Umur":
			qs = qs.filter(kat_pasien__umur__iexact=umur_query)

		if is_valid_queryparam(dateStart_query):
			qs = qs.filter(kode__tanggal__gte=dateStart_query)

		if is_valid_queryparam(dateEnd_query):
			qs = qs.filter(kode__tanggal__lt=dateEnd_query)

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
				qsPkm = qs.values('kode__kode_pkm', 'kode__kode_pkm__nama_pkm').annotate(kasus=Sum(F('kasus_lama') + F('kasus_baru')))
				qsKec = qs.values('kode__kode_pkm__kode_kec', 'kode__kode_pkm__kode_kec__nama_kec').annotate(kasus=Sum(F('kasus_lama') + F('kasus_baru')))
				qsChartUmur = qs.values('kat_pasien__umur').annotate(kasus=Sum(F('kasus_lama') + F('kasus_baru'))).order_by('-kasus')[:10]
				qsChartGender =qs.values('kat_pasien__jenis_kelamin').annotate(kasus=Sum(F('kasus_lama') + F('kasus_baru')))
				qsChartDate =qs.values('kode__tanggal').annotate(kasus=Sum(F('kasus_lama') + F('kasus_baru'))).order_by('kasus')[:10]
		
			if "." in kodePenyakit:
				if jenisKasus_query == "Kasus Baru":
					qsChartPenyakit = qs.values('icd_10__nama_subkat').annotate(kasus = Sum('kasus_baru')).order_by('kasus')[:10]
				elif jenisKasus_query=="Kasus Lama":
					qsChartPenyakit = qs.values('icd_10__nama_subkat').annotate(kasus = Sum('kasus_lama')).order_by('kasus')[:10]
				elif jenisKasus_query=="Semua Jenis":
					qsChartPenyakit = qs.values('icd_10__nama_subkat').annotate(kasus=Sum(F('kasus_lama') + F('kasus_baru'))).order_by('kasus')[:10]
			else:
				if jenisKasus_query == "Kasus Baru":
					qsChartPenyakit = qs.values('kat__nama_kat').annotate(kasus = Sum('kasus_baru')).order_by('kasus')[:10]
				elif jenisKasus_query=="Kasus Lama":
					qsChartPenyakit = qs.values('kat__nama_kat').annotate(kasus = Sum('kasus_lama')).order_by('kasus')[:10]
				elif jenisKasus_query=="Semua Jenis":
					qsChartPenyakit = qs.values('kat__nama_kat').annotate(kasus=Sum(F('kasus_lama') + F('kasus_baru'))).order_by('kasus')[:10]

		qsChartPkm = qsPkm.order_by('-kasus')[:10]
		qsChartKec = qsKec.order_by('-kasus')[:10]
		distNormPkm = qsPkm.aggregate(Max('kasus'), Min('kasus'))
		distNormKec = qsKec.aggregate(Max('kasus'), Min('kasus'))
		#hasilClust = clustering(qsKec, gender_query)
		#print(hasilClust)

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
		}
		global iClustering
		iClustering ={
			'queryKec' : list(qsKec),
			'gender' : gender_query
		}
		return render (request, 'app_BHGIS/indexV2.html', data)

	return render (request, 'app_BHGIS/indexV2.html')

class dataFiltering(View):
	def get(self, request):
		return JsonResponse(iClustering)
		
def get_data(request):
	"""
	data = Kasus.objects.select_related('kode__kode_pkm')\
	.values('kode__kode_pkm', 'kode__kode_pkm__nama_pkm')\
	.annotate(kasus = Sum('kasus_baru'))
	response = json.dumps(list(data))
	"""
	response = json.dumps(list(qsFiltering))
	return HttpResponse(response)

class ChartData(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		data = {
			"male_data" : [23,30,21,26,24,13,24],
			"label_data": ['N','A','D','I','A','Z','K'],
			"gender" : ['Laki-laki', 'perempuan'],
			"gender_data" : [30, 12]
		}
		return Response(data)

def is_valid_queryparam(param):
	return param != '' and param is not None

class CobaView01(View):
	def get(self, request):
		qs = Kecamatan.objects.values('kode_kec', 'nama_kec', 'lat', 'longt')
		qs2 = Kecamatan.objects.values('kode_kec', 'nama_kec', 'jml_pddk', 'pddk_l', 'pddk_p')

		data ={
			'query1' : list(qs),
			'query2' : list(qs2)
		}
		return JsonResponse(data)
	
class SearchView(ListView):
	template_name = 'app_trialv12/tesdatav1.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['query'] = self.request.GET.get('q')
		return context

	def get_queryset(self):
		request = self.request
		query = request.GET.get('q', None)

		if query is not None:
			wilayah_results     	= Kasus.objects.filterWilayah(query)
			penyakit_results     	= Kasus.objects.filterPenyakit(query)
			jeniskelamin_results    = Kasus.objects.filterJenisKelamin(query)
			umur_results     		= Kasus.objects.filterUmur(query)
			periode_results     	= Kasus.objects.filterPeriode(query)

			queryset_chain = chain(
			        wilayah_results,
			        penyakit_results,
			        jeniskelamin_results,
			        umur_results,
			        periode_results)

			qs = sorted(queryset_chain, reverse=True)
			self.count = len(qs) # since qs is actually a list
			return qs
		return Kasus.objects.none() # just an empty queryset as default

def getWilayah(request):
	dataWilayah = Kasus.objects.filterWilayah(request)
	return render (request, 'app_trialv17/tesdatav1.html', {'dataWilayah':dataWilayah})

class PasienAPI(APIView):
	def get(self, request):
		pasiens = Pasien.objects.all()
		serializer = PasienSerializer(pasiens, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = PasienSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PuskesmasView(generics.ListAPIView):
	queryset = Puskesmas.objects.all()
	serializer_class = PuskesmasSerializer
	filter_backends = [SearchFilter]
	search_fields = ['nama_pkm']

class IndeksView(generics.ListCreateAPIView):
	serializer_class = IndeksSerializer
	#pagination_class = 10

	def get_queryset(self, *args, **kwargs):
		queryset_list = Indeks.objects.all()
		query = self.request.GET.get("filter")
		if query:
			queryset_list = queryset_list.filter(
				Q(kode__icontains=query)|
				Q(tanggal__icontains=query)
				)
		return queryset_list

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

class FilterAPIView(generics.ListCreateAPIView):
	queryset = Kasus.objects.all()
	serializer_class = KasusSerializer

class BHGIS_API_Subkat(generics.ListCreateAPIView):
	queryset = Kasus.objects.all()
	serializer_class = KasusSerializer
	pagination_class = PageNumberPagination
	filter_backends = [SearchFilter]
	search_fields = ['kode', 'kat_pasien']

class BHGIS_API_Kat(generics.ListCreateAPIView):
	queryset = Jumlah_Kategori.objects.all()
	serializer_class = JumlahKategoriSerializer

# Disease Clustering
"""
packageNames = ('SpatialEpi', 'dplyr')
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1)

packnames_to_install = [x for x in packageNames if not rpackages.isinstalled(x)]

if len(packnames_to_install) > 0:
    utils.install_packages(StrVector(packnames_to_install))

SpatialEpi = rpackages.importr('SpatialEpi')
dplyr = rpackages.importr('dplyr')

latlong2grid, expected, kulldorff = SpatialEpi.latlong2grid, SpatialEpi.expected, SpatialEpi.kulldorff
pull = dplyr.pull

def clustering(queryset, jenis_kelamin):
	geo_dict = Kecamatan.objects.values('kode_kec', 'nama_kec', 'lat', 'longt')
	data_dict = Kecamatan.objects.values('kode_kec', 'nama_kec', 'jml_pddk', 'pddk_l', 'pddk_p')
	geo = pd.DataFrame.from_dict(geo_dict)
	data = pd.DataFrame.from_dict(data_dict)

	data.insert(1, 'kasus', 0, True)

	length_d = len(data)
	length_q = len(queryset)
	for i in range(length_d):
		for k in range(length_q):
			if data.loc[i, 'kode_kec'] == queryset[k]['kode_kec']:
				data.loc[i, 'kasus'] = queryset[k]['kasus']

	with localconverter(ro.default_converter + pandas2ri.converter):
		geo_r = ro.conversion.py2rpy(geo[['longt','lat']])
		data_r = ro.conversion.py2rpy(data)

	geo_r_grid = latlong2grid(geo_r)

	if jenis_kelamin == 'laki-laki':
		pop = pull(data_r, 'pddk_l')
	elif jenis_kelamin == 'perempuan':
		pop = pull(data_r, 'pddk_p')
	else:
		pop = pull(data_r, 'jml_pddk')

	pop_upper_bound = 0.14
	n_simulations = 999
	alpha_level = 0.05
	plot = False

	binomial = kulldorff(geo_r_grid, pull(data_r, 'kasus'), pop, NULL, pop_upper_bound, n_simulations, alpha_level, plot)

	loc_id = np.array(binomial.rx2("most.likely.cluster").rx2("location.IDs.included"))

	cluster_loc = []
	for i in range(len(loc_id)):
		cluster_loc.append(pull(data_r, 'kode_kec')[(loc_id[i]-1).item()])

	return cluster_loc

"""