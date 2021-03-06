"""middleman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from mm_manager import views as mm_views

urlpatterns = [
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('admin/', admin.site.urls),
    path('mm-register/', mm_views.mm_register, name='mm_register'),
    path('create-trade/', mm_views.create_trade, name='create_trade'),
    path('trade-details/<int:id>/', mm_views.trade_details, name='trade_details'),
    path('trades/', mm_views.view_trades, name='trades'),
    path('signup/', mm_views.signup, name='signup'),
    path('', mm_views.index, name="index"),
]
