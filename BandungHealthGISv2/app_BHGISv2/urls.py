from django.conf.urls import url, include
from app_BHGISv2 import views
from rest_framework.routers import DefaultRouter

urlpatterns =[
	url(r'^index/', views.index, name='index'),
	url(r'^data/graph/', views.get_data, name='dataGraph'),
	url(r'^ChartData/', views.ChartData.as_view()),
	url(r'^dataFiltering/', views.dataFiltering.as_view()),
	url(r'^PasienAPI/', views.PasienAPI.as_view()),
	url(r'^FilterAPIView/', views.FilterAPIView.as_view()),
	url(r'^PenyakitSubkat/', views.PenyakitSubkat.as_view()),
	url(r'^PenyakitKat/', views.PenyakitKat.as_view()),
	url(r'^Puskesmas/', views.Puskesmas.as_view()),
	url(r'^Kecamatan/', views.Kecamatan.as_view()),
	url(r'^SearchView/', views.SearchView.as_view()),
	url(r'^PuskesmasView/', views.PuskesmasView.as_view()),
	url(r'^IndeksView/', views.IndeksView.as_view()),
	url(r'^CobaView01/', views.CobaView01.as_view()),
	url(r'^BHGIS/API/Subkat/', views.BHGIS_API_Subkat.as_view()),
	url(r'^BHGIS/API/Kat/', views.BHGIS_API_Kat.as_view()),
]