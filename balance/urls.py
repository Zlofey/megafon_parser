from django.urls import path

from . import views

app_name = 'balance'
urlpatterns = [
    # ex: /hello/
    #path('hello/', views.index, name='hello'),
    #path('', views.index, name='hello'),
    #path('balance', views.balance, name='balance'),
    path('', views.balance, name='balance'),
    path('line-chart/<int:key>/', views.line_chart, name='line_chart'),
    #path('get_balance', views.get_balance, name='get_balance')
]
