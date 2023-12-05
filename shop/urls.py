from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:category>', views.category_index, name='category'),
    path('look/<slug:product>', views.look_product, name='product'),
]