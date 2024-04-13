from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import include
from .views import filter_products
from .views import my_orders

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login_view,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.userLogout,name='logout'),
    path('m_register/',views.mregister,name='m_register'),
    path('dashboard1.html/',views.dashboard1,name='dashboard1'),
    path('dashboard2.html/',views.dashboard2,name='dashboard2'),
    path('mdashboard2.html/',views.mdashboard2,name='mdashboard2'),

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
    # mend and women_only
    path('menonly/', views.menonly, name='men_only'),
    path('womenonly/', views.womenonly, name='women_only'),
    path('kidsonly/', views.kidsonly, name='kids_only'),   
    # wishlist
    path('add_wishlist/<int:product_id>/', views.add_wishlist, name='add_wishlist'),
    path('delete_wishlist/<int:product_id>/', views.delete_wishlist, name='delete_wishlist'),
    path('wishlist_view/',views.wishlist_view,name='wishlist_view'),
    # Cart
    
    
    # path('cart',views.cart,name="cart"), 
    # path('increase_item/<int:item_id>/', views.increase_item, name='increase_item'),
    # path('decrease_item/<int:item_id>/', views.decrease_item, name='decrease_item'),
    # path('add_cart1/<int:bookid2>/', views.add_cart1, name='add_cart1'),
    # path('delete_cart/<int:bookid2>/', views.delete_cart, name='delete_cart'),
    # path('add_cart/<int:bookid2>/', views.add_cart, name='add_cart'),
    
    
    
    # search
    path('search_product/',views.search_product,name='search_product'),
    # manage categories
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    # view added product
    # path('view_edit_product/<int:product_id>/', views.view_edit_product, name='view_edit_product'),
    # path('product_management/', views.product_management, name='product_management'),
    path('product_list/', views.product_list, name='product_list'),
    # path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    # path('activate_product/<int:product_id>/', views.activate_product, name='activate_product'),
    # path('deactivate_product/<int:product_id>/', views.deactivate_product, name='deactivate_product'),
    
    path('delete_wishlist1/<int:product_id>/', views.delete_wishlist1, name='delete_wishlist1'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # filter
    path('filter/', filter_products, name='filter_products'),
    
    # 
    # path('buyNowComplete/<int:product_id>/', views.buyNowComplete, name='buyNowComplete'),
    path('order_placed/', views.order_placed, name='order_placed'),
    path('order_details/',views.order_details,name='order_details'),
    path('stock_details/', views.stock_details, name='stock_details'),
    path('shippingaddress/', views.shipping_address, name='shippingaddress'),








    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/', views.view_cart, name='cart'),
    path('increase-cart-item/<int:product_id>/', views.increase_cart_item, name='increase-cart-item'),
    path('decrease-cart-item/<int:product_id>/', views.decrease_cart_item, name='decrease-cart-item'),
    path('fetch-cart-count/', views.fetch_cart_count, name='fetch-cart-count'),
    path('create-order/', views.create_order, name='create-order'),
    path('summery/', views.summery, name='summery'),
    path('handle-payment/', views.handle_payment, name='handle-payment'),
    path('order_complete/', views.order_complete, name='order_complete'),
    
    
    
    
    

    # main Project
    path('add_agent/',views.add_agent,name='add_agent'),
    path('my-orders/',my_orders, name='my_orders'),
    path('rating/<int:product_id>/', views.rating, name='rating'),
    path('rating0/<int:product_id>/', views.rating0, name='rating0'),

    path('adashboard.html/',views.adashboard,name='adashboard'),
    path('astock_details/', views.astock_details, name='astock_details'),

    # Chat
    path('messages_page/', views.messages_page, name='messages_page'),
    path('agent_profile.html/',views.agent_profile,name='agent_profile'),

    # Product Comparison
    path('add_to_compare/<int:product_id>/', views.add_to_compare, name='add_to_compare'),
    path('compare/', views.compare_product, name='compare_product'),
    path('remove_product/<int:product_id>/', views.remove_product, name='remove_product'),

    # Product Edit & Desiable
    path('update/<int:pk>/', views.update_product, name='update_product'),
    path('disable/<int:pk>/', views.disable_product, name='disable_product'),
    path('enable/<int:pk>/', views.enable_product, name='enable_product'),
    path('clear_all_notifications/', views.clear_all_notifications, name='clear_all_notifications'),
    path('stock_details1/', views.stock_details1, name='stock_details1'),
    
    # New Arrivals
    path('add_new_arrival/', views.add_new_arrival, name='add_new_arrival'),
    path('new-arrivals/', views.new_arrival_list, name='new_arrival_list'),
    path('new-arrival/<int:pk>/edit/', views.new_arrival_edit, name='new_arrival_edit'),
    path('new-arrival/<int:pk>/delete/', views.new_arrival_delete, name='new_arrival_delete'),
    path('view_arrival/', views.view_arrival, name='view_arrival'),


    # Return Product
    path('return-product/', views.return_product, name='return_product'),
    path('view-returns/', views.view_returns, name='view_returns'),
    path('returned_product_list/', views.returned_product_list, name='returned_product_list'),
    
    # Seminar
    path('process-image/', views.process_image, name='process_image'),
    
    # order details
    path('order_product/', views.order_product, name='order_product'),
    
    # Delivery
    path('order_delivery/', views.order_delivery, name='order_delivery'),
    
    path('delivery_details/<int:order_id>/', views.delivery_details, name='delivery_details'),
    path('delivery_success/', views.delivery_success, name='delivery_success'),
    
    path('otp_verification/<int:order_id>/', views.otp_verification, name='otp_verification'),
    path('update_delivery_status/<int:order_id>/', views.update_delivery_status, name='update_delivery_status'),
    
    ]