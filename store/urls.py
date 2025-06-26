
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('starter/',views.starter_page,name='starter'),
    path('book_table/',views.book_table,name='book_table'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('leave/<int:booking_id>/',views.leave_table,name='leave_table'),
    path('menu/', views.menu_order, name='menu_order'),
    path('history/',views.history_view,name='history')
]
