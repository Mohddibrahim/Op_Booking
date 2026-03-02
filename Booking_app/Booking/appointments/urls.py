from django.urls import path
from .views import*


urlpatterns = [
    
path('slot/create/', create_slot, name='create_slot')
]

