from django.urls import path
from . import views

app_name = 'store_control'

urlpatterns = [
    path('stores/', views.store, name="stores_url"),
    path('stores/<str:name>', views.store_detail, name="detail_url"),
    path('stores/<str:name>/add_product', views.add_product_to_store, name="add_to_store")
]

