from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add-business/', views.add_business_view, name='add_business'),
    path('addBusinessDetails/', views.add_business_view, name='add_business_alt'),
    path('website/<int:id>/', views.view_website, name='view_website'),
    path('website/raw/<int:id>/', views.raw_website, name='raw_website'),
    path('website/download/<int:id>/', views.download_website, name='download_website'),
    path('business/delete/<int:id>/', views.delete_business_view, name='delete_business'),
]
