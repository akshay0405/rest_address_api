
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('get_pincode/<str:state>/<str:district>/<str:taluk>',views.GetPincode.as_view(),name="pincodeurl"),
   path('get_pincode/<str:state>/<str:district>/<str:taluk>/<str:office>',views.GetPincode1.as_view(),name="pincodeurl"),
   path('get_towns',views.GetTowns.as_view(),name="townurl"),
   path('get_districts',views.GetDistrictname.as_view(),name="districturl"),
   path('get_states',views.GetStatelist.as_view(),name="stateurl"),

]
