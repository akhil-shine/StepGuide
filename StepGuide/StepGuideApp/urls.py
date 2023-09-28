from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    # path('shop/',views.shop,name='shop'),
    # path('shopsingle/',views.shopsingle,name='shop1'),
    path('login/',views.login_view,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.userLogout,name='logout'),
    path('m_register/',views.mregister,name='m_register'),
    path('admindashboard/',views.admindashboard,name='admindashboard'),
    path('merchant_dashbord/',views.merchant_dashbord,name='merchant_dashbord'),
    path('buy/',views.buy,name='buy'),
    path('purchase/',views.purchase,name='purchase'),
    path('admindashboard/dashboard.html/',views.dashboard,name='dashboard'),
    path('edit_profile.html/',views.edit_profile,name='edit_profile'),
]