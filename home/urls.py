from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('test/', views.test, name='test'),
    path('details/<slug:slug>/',views.exp_details, name='exp-details' ),
    path('favourite/<int:id>/',views.favourite,name='favourite'),
    path('favourites/', views.favourite_list, name='favourite_list'),
    path('supply/', views.supply, name='supply'),
    path('supply_details/<int:id>/<slug:slug>/',views.supply_details, name='supply-details' ),
    path('addcomment/<int:id>/',views.addcomment,name='addcomment'),
    path('filter-data',views.filter_data,name='filter_data'),
 
]