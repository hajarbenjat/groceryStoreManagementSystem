from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'), 
    path('inventory/', views.inventory, name='inventory'),
    path('add_product/', views.add_product, name='add_product'),
    path('make_sale/', views.make_sale, name='make_sale'),
]
