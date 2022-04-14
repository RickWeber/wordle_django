from django.urls import path

from . import views

urlpatterns = [ 
    path('index/', views.index, name=''), 
    path('', views.Guess.as_view(), name='guess'),
    path('cheat/', views.cheat, name='cheat')
]
