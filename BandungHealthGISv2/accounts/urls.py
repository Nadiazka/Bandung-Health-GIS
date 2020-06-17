from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login/', views.loginPage, name="login"),
    url(r'^register/', views.registerPage, name="register"),
    url(r'^logout/', views.logoutUser, name="logout"),
]