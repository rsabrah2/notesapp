from django.urls import path
from . import views

"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# URLs in the app folder must be mapped to the project urls.py files by type
# path('', include('[app].urls')),
# URLs in the app folder must be mapped to the project urls.py files by type
# path('', include('[app].urls')),
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('notes/', views.list_notes,name='list_notes'),
    path('simple/', views.sampleForm, name='sampleForm')


]