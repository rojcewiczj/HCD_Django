from . import views
from django.urls import path
 
urlpatterns = [
    path('form_builder/', views.index) #our-domain.com/form_builder,
]