from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.new_account, name='new-account'),
    path('contact',views.contact_us, name='contact_us'),
    path('cart', views.cart, name='cart'),
    path('login', views.login, name='login'),
    path('product-details', views.product_details, name='product-details'),
    path('checkout' , views.checkout , name = 'checkout' ),
    path('confirmation' , views.get_info , name = 'confirmation' ),
    path('history' , views.history , name = 'history' )

#path('/test', views.index, name='index'),
]