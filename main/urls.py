"""adwebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^about/$', views.about, name = 'about'),
	url(r'^establishments/$', views.establishments, name = 'establishments'),
	url(r'^login/$', views.loginView, name = 'login'),
	url(r'^logout/$', views.logoutView, name = 'logout'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^dashboard/$', views.dashboard, name = 'dashboard'),
    url(r'^delete/(?P<adid>\d+)/$', views.deleteAd, name = 'deletead'),
    url(r'^approve/(?P<adid>\d+)/$', views.approveAd, name = 'approvead'),
    url(r'^checkmail/$', views.checkMail, name = 'checkmail'),
    url(r'^register/resend_validation/$', views.resendMail, name='resendmail'),
    url(r'^forgotpassword/$', views.forgotPass, name='forgotpass'),
    url(r'^changepassword/$', views.changePass, name='changepass'),
    url(r'^uploadad/$', views.uploadAd, name='uploadad'),
    url(r'^events/$', views.events, name = 'events'),
    url(r'^uploadevent/$', views.uploadEvent, name='uploadevent'),
    url(r'^deleteevent/(?P<adid>\d+)/$', views.deleteEvent, name = 'deletead'),
    url(r'^approveevent/(?P<adid>\d+)/$', views.approveEvent, name = 'approvead'),
]
