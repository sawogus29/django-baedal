from django.urls import path

from . import views

app_name = 'baedal' # namespace
urlpatterns = [
  path('', views.index, name = 'index'),
]