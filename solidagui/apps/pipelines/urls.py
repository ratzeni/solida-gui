from django.urls import path

from . import views

urlpatterns = [
    path('browse/', views.BrowseView.as_view(), name='pipelines.browse'),
    path('refresh/', views.refresh, name='pipelines.refresh'),
    path('add_new/', views.add_new, name='pipelines.add_new'),
    path('<pipeline_id>/setup/', views.setup, name='pipeline.setup'),
    path('<pipeline_id>/deploy/', views.deploy, name='pipeline.deploy'),
]
