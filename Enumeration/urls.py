from django.urls import path
import Enumeration.views as views

urlpatterns = [
    path('', views.index, name='index'),

    # Dara API urls
    path('db/<str:domain>/', views.db_domain, name="db_domain"),
    
    # Enumeration API urls
    path('enum/passive/<str:domain>/', views.passive_enum_domain, name="passive_enum_domain"),
    path('enum/active/<str:domain>/', views.active_enum_domain, name="active_enum_domain"),
    
    # Domain API urls 
    path('domain/info/<str:domain>/', views.info_db_domain, name="info_db_domain"),
    path('domain/delete/<str:domain>/', views.delete_db_domain, name="delete_db_domain"),
]