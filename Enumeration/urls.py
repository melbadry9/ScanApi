from django.urls import path
import Enumeration.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('db/<str:domain>/', views.db_domain, name="db_domain"),
    path('enum/passive/<str:domain>/', views.passive_enum_domain, name="passive_enum_domain"),
    path('enum/active/<str:domain>/', views.active_enum_domain, name="active_enum_domain"),
]