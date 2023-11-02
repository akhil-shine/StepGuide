from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import include

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
    # path('admindashboard/',views.admindashboard,name='admindashboard'),
    # path('merchant_dashbord/',views.merchant_dashbord,name='merchant_dashbord'),
    path('dashboard1.html/',views.dashboard1,name='dashboard1'),
    path('dashboard2.html/',views.dashboard2,name='dashboard2'),
    path('edit_profile.html/',views.edit_profile,name='edit_profile'),
    # Forget Password
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    # 
    path('userview.html/',views.userview,name='userview'),
    path('updateStauts/<int:update_id>',views.updateStatus,name="updateStatus"),
    path('deleteUser/<int:delete_id>',views.deleteUser,name="deleteUser"),
    path('', include("allauth.urls")), #most important,
    path('accounts/profile/', views.index, name='index'),
    # Active and Disable Account
    path('disable_account/<int:update_id>/', views.disableAccount, name='disable_account'),
    path('enable_account/<int:update_id>/', views.enableAccount, name='enable_account'),
    path('add_category/',views.newcategory,name='add_category'),
    path('add_subcategory/',views.newsubcategory,name='add_subcategory'),
    path('sellerindex/',views.sellerindex,name='sellerindex'),
    path('categoryajax/<str:category>/', views.categoryajax, name='categoryajax'),
    path('get_subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),
    # view product in page
    path('productlist/', views.productlist, name='productlist'),
    path('purchase/<int:product_id>/', views.purchase, name='purchase'),
    
    
]