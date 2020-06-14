from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login/', views.loginPage, name="login"),
    url(r'^register/', views.registerPage, name="register"),
    url(r'^logout/', views.logoutUser, name="logout"),
    url(r'^edit/profile/', views.editProfile, name="editProfile"),
    url(r'^change/password/', views.changePasswordPage, name="changePass"),
]