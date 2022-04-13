from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.index, name=''), 
    path('guess/', views.Guess.as_view(), name='guess'),
    path('cheat/', views.cheat, name='cheat')
]
