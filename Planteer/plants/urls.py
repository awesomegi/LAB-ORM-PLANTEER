from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.all_plants, name='all_plants'),
    path('<int:plant_id>/detail/', views.plant_detail, name='plant_detail'),
    path('new/', views.new_plant, name='new_plant'),
    path('<int:plant_id>/update/', views.update_plant, name='update_plant'),
    path('<int:plant_id>/delete/', views.delete_plant, name='delete_plant'),
    path('search/', views.search, name='search'),
]
