from django.urls import path

from . import views

app_name = 'baedal' # namespace
urlpatterns = [
  path('', views.index, name = 'index'),
  # common
  path('signout', views.signout, name='signout'),
  
  # customer
  path('customer/signin', views.customer_signin, name='customer_signin'),
  path('customer/signup', views.customer_signup, name='customer_signup'),
  path('customer/home', views.customer_home, name='customer_home'),

  # restaurant
  path('restaurant/signin', views.restaurant_signin, name='restaurant_signin'),
  path('restaurant/signup', views.restaurant_signup, name='restaurant_signup'),
  path('restaurant/menus', views.restaurant_menus, name='restaurant_menus'),
  path('restaurant/new_menu', views.new_menu, name='new_menu'),
]