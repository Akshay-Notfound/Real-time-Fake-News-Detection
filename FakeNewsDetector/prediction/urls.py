from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path('batch_predict/', views.predict_batch, name='predict_batch'),
    path('latest_news/', views.latest_news, name='latest_news'),
]
