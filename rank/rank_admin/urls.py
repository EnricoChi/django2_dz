from django.urls import path

from rank_admin import views

app_name = 'rank_admin'

urlpatterns = [
    path('', views.admin_main, name='main'),

    path('company/all/', views.CompanyAll.as_view(), name='company-all'),
    path('company/add/', views.CompanyAdd.as_view(), name='company-add'),
    path('company/edit/<int:pk>', views.CompanyEdit.as_view(), name='company-edit'),
    path('company/delete/', views.company_del, name='company-del'),

    path('company/category/all/', views.CompanyCategoryAll.as_view(), name='category-all'),
    path('company/category/add/', views.CompanyCategoryAdd.as_view(), name='category-add'),
    path('company/category/edit/<int:pk>', views.CompanyCategoryEdit.as_view(), name='category-edit'),
    path('company/category/delete/', views.company_category_del, name='category-del'),
]
