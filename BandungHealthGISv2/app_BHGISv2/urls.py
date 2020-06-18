from django.conf.urls import url, include
from app_BHGISv2 import views
from rest_framework.routers import DefaultRouter

urlpatterns =[
	url(r'^$', views.index, name='index'),
	url(r'^data/graph/', views.get_data, name='dataGraph'),
	url(r'^dataFiltering/', views.dataFiltering.as_view()),
	url(r'^PenyakitSubkat/', views.PenyakitSubkat.as_view()),
	url(r'^PenyakitKat/', views.PenyakitKat.as_view()),
	url(r'^Puskesmas/', views.Puskesmas.as_view()),
	url(r'^Kecamatan/', views.Kecamatan.as_view()),
	url(r'^DataClustering/', views.DataClustering.as_view()),
]