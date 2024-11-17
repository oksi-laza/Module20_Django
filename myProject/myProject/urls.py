"""
URL configuration for myProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myApp.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page),
    path('contact_form/', contact_form),
    path('form_of_record/', form_of_record),
    path('form_of_record/update_previous_appointment/', update_previous_appointment),
    path('form_of_record/no_changes_previous_appointment/', no_changes_previous_appointment),
    path('foundation/', foundation),
    path('katalog_proektov_domov/', katalog_proektov_domov),
    path('septic_tanks/', septic_tanks),
    path('o_kompanii/', o_kompanii),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
