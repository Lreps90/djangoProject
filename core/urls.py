from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('code_editor/', views.code_editor, name='code_editor'),
    path('api/save/', views.save_data, name='save_data'),
    path('download/', views.download_file, name='download_file'),
    path('run_stream/', views.run_code_stream, name='run_code_stream'),
]

